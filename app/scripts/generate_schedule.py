from app.scripts.AssignmentSchedule import AssignmentsSchedule
from app.scripts.extract import get_data

def generate_data():
    assignments,classrooms,courses,professors = get_data()
    schedule = AssignmentsSchedule(
        courses=courses,assignments=assignments,
        classrooms=classrooms,professors=professors
    )
    data = schedule.init()
    #return data
    return []