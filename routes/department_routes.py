from flask import jsonify, request, Blueprint
from extension import db
from models.department import Department

department_bp = Blueprint(
    "department",
    __name__,
    url_prefix="/department"
)

# ➕ Add Department
@department_bp.route("/add", methods=["POST"])
def add_department():
    data = request.get_json()

    # error handling for empty name
    if not data or not data.get("name"):
        return jsonify({"error": "Department name is required"}), 400

    # duplicate name check
    existing_name = db.session.query(Department).filter_by(
        name=data["name"]
    ).first()

    if existing_name:
        return jsonify(
            {"error": "Same name departments are not possible"}
        ), 409

    new_department = Department(name=data["name"])

    db.session.add(new_department)
    db.session.commit()

    return jsonify({
        "message": f"{new_department.name} department added successfully"
    }), 201


# 📋 List Departments
@department_bp.route("/all", methods=["GET"])
def list_departments():
    departments = db.session.query(Department).all()

    return jsonify([
        {
            "id": d.id,
            "name": d.name
        }
        for d in departments
    ])

