
from app.db.database import get_entity_by_id,SessionLocal
from app.db.models import (Course,CareerCourse,Assignment)
from sqlalchemy.orm import joinedload
from app.db.response_models import (
    CourseModel
)

def repository_get_all():
    db = SessionLocal()
    data = db.query(Course).order_by(Course.Id).all()
    resp = [ CourseModel(id=x.Id,semester=x.Semester,name=x.Name, id_career=-1) for x in data]
    db.close()
    return resp

def repository_get_courses_by_student(id):
    db = SessionLocal()
    data = db.query(Assignment).options(joinedload(Assignment.course)).filter(Assignment.Id_student == id).all()
    resp = [ CourseModel(id=x.course.Id,semester=x.course.Semester,name=x.course.Name, id_career=-1) for x in data]
    db.close()
    return resp

def repository_save_course(entity:CourseModel):
    session = SessionLocal()
    if entity.id == -1:
        obj = Course(Name=entity.name,Semester=entity.semester)
        session.add(obj)
        
    else:
        obj:Course= session.query(Course).get(entity.id)
        obj.Semester = entity.semester
        obj.Name = entity.name
    session.commit()
    

    #Remove
    if entity.id_career and not entity.id_career == -1:
        assigs = session.query(CareerCourse).filter(CareerCourse.Id_course == obj.Id).all()
        for assig in assigs:
            session.delete(assig)
            session.commit()
        new_assign = CareerCourse(Id_career = entity.id_career, Id_course = obj.Id)
        session.add(new_assign)
        session.commit()
        session.close()
    
    return entity

def repository_delete_course(entity:CourseModel):
    session = SessionLocal()
    obj = session.query(Course).get(entity.id)
    session.delete(obj)
    session.commit()
    session.close()
    return entity