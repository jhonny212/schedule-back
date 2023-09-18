
from app.db.database import get_entity_by_id,SessionLocal,session
from app.db.models import (Student,Career,Course,Assignment)
from sqlalchemy.orm import joinedload

from app.db.response_models import (
    StudentModel,CareerModel,AssigmentModel
)

def repository_save_students(entity:StudentModel):
    student:Student = session.query(Student).get(entity.carnet)
    if not student:
        student = Student(Carnet=entity.carnet,Id_career=entity.career.code,Semester=entity.semester,Name=entity.name)
        session.add(student)
    else:
        student.Id_career = entity.career.code
        student.Name = entity.name
        student.Semester = entity.semester
    session.commit()
    return entity

def repository_delete_students(entity:StudentModel):
    student = session.query(Student).get(entity.carnet)
    session.delete(student)
    session.commit()
    return entity

def repository_assign_course(body:AssigmentModel):
    assign: Assignment = Assignment(Id_section=body.section,Id_course=body.id_course,Id_student=body.id_student)
    session.add(assign)
    session.commit()
    return body

def repository_remove_assignment(student,course):
    assig = session.query(Assignment).filter(Assignment.Id_course == course ).filter(Assignment.Id_student == student).first()
    if assig:
        session.delete(assig)
    session.commit()
    

def repository_get_studentss():
    db = SessionLocal()
    result = db.query(Student).options(joinedload(Student.career)).order_by(Student.Carnet).all()
    resp =  [
        StudentModel(career=CareerModel(code=x.career.Code,extension=x.career.Extension,name=x.career.Name),semester=x.Semester,carnet=x.Carnet,name=x.Name) for x in result
    ]
    db.close()
    return resp