
from app.db.database import get_entity_by_id,SessionLocal,session
from app.db.models import (Course)

from app.db.response_models import (
    CourseModel
)

def repository_get_all():
    db = SessionLocal()
    data = db.query(Course).order_by(Course.Id).all()
    resp = [ CourseModel(id=x.Id,semester=x.Semester,name=x.Name) for x in data]
    db.close()
    return resp

def repository_save_course(entity:CourseModel):
    if entity.id == -1:
        obj = Course(Name=entity.name,Semester=entity.semester)
        session.add(obj)
    else:
        obj:Course= session.query(Course).get(entity.id)
        obj.Semester = entity.semester
        obj.Name = entity.name
    session.commit()
    return entity

def repository_delete_course(entity:CourseModel):
    obj = session.query(Course).get(entity.id)
    session.delete(obj)
    session.commit()
    return entity