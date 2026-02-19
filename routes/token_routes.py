from flask import Blueprint, request, jsonify
from sqlalchemy import func
from extension import db
from models.token_model import Token
from models.patient import Patient
from models.department import Department

from services.queue_manager import get_next_patient
from services.helpers import token_to_dict
from services.analytics import calculate_statistics
from services.ml_engine import predict_wait_time
from services.notification_engine import notify_if_near_turn
from services.helpers import token_to_notification_dict





token_bp=Blueprint("token",__name__,url_prefix="/token")

@token_bp.route("/genrate",methods=["POST"])
def generate_token():
    data=request.get_json()
    
    if not data or not data.get("patient_id") or not data.get("department_id"):
        return jsonify({
            "error": "patient_id and department_id are required"
        }), 400
        
    patient_id=data['patient_id']
    department_id=data['department_id']
    
    #checking patient
    patient=db.session.get(Patient,patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    # check department exists
    department = db.session.get(Department, department_id)
    if not department:
        return jsonify({"error": "Department not found"}), 404
    
    #get last token number for this department
    
    #here we use this query function because we want to find max token number of any department so this method works and scalar gives single value
    last_token_number=db.session.query(func.max(Token.token_number)).filter_by(department_id=department_id).scalar()

    if last_token_number is None:
        next_token_number = 1
    else:
        next_token_number = last_token_number + 1

    
    new_token = Token(
        token_number=next_token_number,
        patient_id=patient_id,
        department_id=department_id
    )

    db.session.add(new_token)
    db.session.commit()

    return jsonify({
        "message": "Token generated successfully",
        "token_number": new_token.token_number,
        "token_id": new_token.id,
        "status": new_token.status
    }), 201
    
#  View Queue for a Department
@token_bp.route("/queue/<int:department_id>", methods=["GET"])
def department_queue(department_id):
    tokens = db.session.query(Token).filter_by(
        department_id=department_id,
        status="WAITING"
    ).order_by(Token.token_number).all()

    return jsonify([
        {
            "token_id": t.id,
            "token_number": t.token_number,
            "patient_id": t.patient_id,
            "status": t.status
        }
        for t in tokens
    ])
    
@token_bp.route("/next/<int:department_id>", methods=["GET"])
def get_next_token(department_id):

    # get all waiting tokens
    tokens = db.session.query(Token).filter_by(
        department_id=department_id,
        status="WAITING"
    ).order_by(Token.token_number).all()

    if not tokens:
        return {"message": "No patients in queue"}, 200

    # convert DB objects → dicts for smart logic
    patients_for_queue = []
    patients_for_notify = []

    for t in tokens:
        patient = db.session.get(Patient, t.patient_id)

        queue_dict = {
            "token_id": t.id,
            "patient_id": patient.id,
            "priority": 2 if t.status == "EMERGENCY" else 1,
            "join_time": t.id
        }

        notify_dict = token_to_notification_dict(t, patient)

        patients_for_queue.append(queue_dict)
        patients_for_notify.append(notify_dict)

    # 🔥 SMART QUEUE DECISION
    next_patient = get_next_patient(patients_for_queue)

    # 🔔 SEND SMS (PLACE 2)
    notify_if_near_turn(patients_for_notify)

    return {
        "next_token_id": next_patient["token_id"],
        "patient_id": next_patient["patient_id"]
    }


@token_bp.route("/analytics/<int:department_id>", methods=["GET"])
def department_analytics(department_id):
    tokens = db.session.query(Token).filter_by(
        department_id=department_id
    ).all()

    data = [{
        "status": t.status.lower(),
        "priority": 2 if t.status == "EMERGENCY" else 1
    } for t in tokens]

    stats = calculate_statistics(data)
    return stats

@token_bp.route("/predict/<int:department_id>", methods=["GET"])
def predict_wait(department_id):
    waiting = db.session.query(Token).filter_by(
        department_id=department_id,
        status="WAITING"
    ).count()

    predicted = predict_wait_time(waiting * 5, doctors=2)

    return {
        "estimated_wait_minutes": predicted
    }
