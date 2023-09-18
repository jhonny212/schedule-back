import pandas as pd
from app.db.models import (CareerCourse,Career)
from app.db.response_models import (
    CareerModel
)

from app.db.database import get_entity_by_id,SessionLocal,session

def repository_get_career_by_course(course):
    db = SessionLocal()
    career = db.query(CareerCourse).filter(CareerCourse.Id_course == course).first()
    if career:
        career = db.query(Career).filter(Career.Code == career.Id_career).first()
        resp = CareerModel(code=career.Code,extension=career.Extension,name=career.Name)
        db.close()
        return resp
    return None

def repository_get_careers():
    db = SessionLocal()
    data = db.query(Career).all()
    resp = [
        CareerModel(code=x.Code,extension=x.Extension,name=x.Name) for x in data
    ]
    db.close()
    return resp
