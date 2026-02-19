from flask import Blueprint, jsonify, request
from extension import db
from models.patient import Patient

patient_bp = Blueprint(
    "patient",
    __name__,
    url_prefix="/patient"
)

@patient_bp.route("/add", methods=["POST"])
def add_patient():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("phone"):
        return jsonify({
            "error": "name and phone number are required"
        }), 400

    phone = data["phone"]

    existing_patient = db.session.query(Patient).filter_by(
        phone=phone
    ).first()

    if existing_patient:
        return jsonify({
            "error": "Phone number already exists"
        }), 409

    new_patient = Patient(
        name=data["name"],
        age=data.get("age"),
        phone=phone
    )

    db.session.add(new_patient)
    db.session.commit()

    return jsonify({
        "message": "Patient added successfully",
        "patient_id": new_patient.id
    }), 201
