
def sort_by_priority(patients):
    """
    Basic priority sorting:
    Emergency first, then by join time 
    """

    return sorted(
       patients,
       key = lambda x: (-x["priority"],x["join_time"]) 
    )

def smart_schedule(patients):
    """
    Smart fair Scheduling Algorithm

    Rule:
    Serve 2 emergency patients,
    then serve 1 normal patient (if available)

    Prevents starvation of normal patients.
    """
    emergency = []
    normal = []

    #  seprate patients by priority 

    for p in patients :
        if p["priority"] == 2:
            emergency.append(p)
        else:
            normal.append(p)
    

# Maintain first in first out inside each group

    emergency.sort(key = lambda x: x["join_time"])
    normal.sort(key = lambda x: x["join_time"])

    scheduled_queue = []
    e_count = 0

    while emergency or normal:

        # Serve up to 2 emergency patients
        while emergency and e_count < 2:
            scheduled_queue.append(emergency.pop(0))
            e_count += 1

        # Serve 1 normal patient if exists
        if normal:
            scheduled_queue.append(normal.pop(0))

        e_count = 0

    return scheduled_queue
    
def get_next_patient(patients):
    """
    Returns next patient based on smart scheduling
    """
    
    if not patients:
        return None
    
    scheduled = smart_schedule(patients)
    return scheduled[0]