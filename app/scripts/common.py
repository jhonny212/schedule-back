from app.db.database import get_entity_by_id
from app.db.response_models import (
    Classroom as ClassroomModel, Schedule as ScheduleModel,
    CourseModel,ProfessorModel,SectionModel
)

from app.db.models import (
    Assignment,Professor,Classroom,CapacibilityProfessor,Course,Section)

def get_classroom_model(classroom_id):
        if classroom_id:
            entity:Classroom = get_entity_by_id(Classroom,int(classroom_id))
            return ClassroomModel(id=entity.Id, name=entity.Name, capacity=entity.Capacity)
        else:
            return None
        
def get_professor_model(professor_id):
    if professor_id:
        entity:Professor = get_entity_by_id(Professor,int(professor_id),Professor.Cui)
        return ProfessorModel(cui=entity.Cui,name=entity.Name,
                                hour_start=entity.Hour_start,hour_end=entity.Hour_end
                                )
    else:
        return None
    

def get_course_model(course_id):
    entity:Course = get_entity_by_id(Course,int(course_id))
    return CourseModel(id=entity.Id, name=entity.Name, semester=entity.Semester, id_career=-1)

def get_section_model(section_id):
    entity: Section = get_entity_by_id(Section,section_id)
    return SectionModel(id=entity.Id,name=entity.Name)