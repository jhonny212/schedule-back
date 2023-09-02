
from app.db.database import get_entity_by_id,SessionLocal,session
from app.db.models import (
    Assignment,Professor,Classroom,Section,Course)

from app.db.response_models import (
    Classroom as ClassroomModel, Schedule as ScheduleModel,
    CourseModel,ProfessorModel,SectionModel
)

def repository_save_classroom(entity:ClassroomModel):
    if entity.id == -1:
        classroom = Classroom(Capacity=entity.capacity,Name=entity.name)
        session.add(classroom)
    else:
        classroom:Classroom = session.query(Classroom).get(entity.id)
        classroom.Capacity = entity.capacity
        classroom.Name = entity.name
    session.commit()
    return entity

def repository_delete_classroom(entity:ClassroomModel):
    classroom = session.query(Classroom).get(entity.id)
    session.delete(classroom)
    session.commit()
    return entity

def repository_get_classrooms():
    db = SessionLocal()
    result = db.query(Classroom).all()
    resp =  [
        ClassroomModel(id=x.Id,name=x.Name,capacity=x.Capacity) for x in result
    ]
    db.close()
    return resp