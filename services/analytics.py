
def calculate_statistics(patients):
    """
    Genrate analytics data for dashboard
    """

    total_patients = len(patients)

    served = [p for p in patients if p["status"] == "served"]
    waiting = [p for p in patients if p["status"] == "waiting"]
    emergency = [p for p in patients if p["priority"] == 2]

    status = {
        "total_patients": total_patients,
        "served_patients": len(served),
        "waiting_patients": len(waiting),
        "emergency_cases": len(emergency)
    }

    return status

    
