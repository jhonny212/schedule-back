
from app.db.database import get_entity_by_id,SessionLocal,session
from app.db.models import (Professor,CapacibilityProfessor,Course)

from app.db.response_models import (
    ProfessorModel,CapacibilityProfessorModel,CourseModel
)

def repository_get_all():
    db = SessionLocal()
    data = db.query(Professor).order_by(Professor.Cui).all()
    resp = [ ProfessorModel(
                cui=x.Cui,name=x.Name,hour_end=x.Hour_end,hour_start=x.Hour_start,
            ) for x in data]
    db.close()
    return resp

def repository_get_assigments(cui):
    db = SessionLocal()
    capabilities = db.query(CapacibilityProfessor).filter_by(Id_professor=cui).order_by(CapacibilityProfessor.Id_professor).all()
    results = []
    for capability in capabilities:
        course = session.query(Course).filter_by(Id=capability.Id_course).first()
        professor = session.query(Professor).filter_by(Cui=capability.Id_professor).first()

        if course and professor:
            result = CapacibilityProfessorModel(course=CourseModel(id=course.Id,semester=course.Semester,name=course.Name),
                                                professor=ProfessorModel(cui=cui,name=professor.Name,hour_end=professor.Hour_end,hour_start=professor.Hour_start),
                                                flag=capability.flag
                                                )
            results.append(result)
    db.close()
    return results

def repository_save_professor(entity:ProfessorModel):
    obj:Professor= session.query(Professor).get(entity.cui)
    if not obj:
        obj = Professor(Name=entity.name,Hour_end=entity.hour_end,
                        Cui=entity.cui,Hour_start=entity.hour_start
                        )
        session.add(obj)
    else:
        obj.Hour_end = entity.hour_end
        obj.Hour_start = entity.hour_start
        obj.Name = entity.name
    session.commit()
    return entity

def repository_delete_professor(entity:ProfessorModel):
    obj = session.query(Professor).get(entity.cui)
    session.delete(obj)
    session.commit()
    return entity

def repository_add_assignment(entity: CapacibilityProfessorModel):
    obj = CapacibilityProfessor(Id_course = entity.course.id, Id_professor = entity.professor.cui, flag = entity.flag)
    session.add(obj)
    session.commit()
    return entity

def repository_remove_assignment(entity: CapacibilityProfessorModel):
    obj = session.query(CapacibilityProfessor).filter_by(Id_course=entity.course.id, Id_professor=entity.professor.cui).first()
    session.delete(obj)
    session.commit()
    return entity