def token_to_dict(token):
    return {
        "token_id": token.id,
        "patient_id": token.patient_id,
        "department_id": token.department_id,
        "status": token.status.lower(),
        "priority": 2 if token.status == "EMERGENCY" else 1,
        "join_time": token.id   # simple FIFO substitute
    }

def token_to_notification_dict(token, patient):
    return {
        "name": patient.name,
        "phone": patient.phone,
        "status": token.status.lower()
    }
