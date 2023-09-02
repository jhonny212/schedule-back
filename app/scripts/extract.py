from app.db.database import excute_query,SessionLocal
from app.db.models import (
    Assignment,Professor,Classroom,CapacibilityProfessor,Course)
import pandas as pd

def extract_element(element):
    data = element.__dict__
    # if '_sa_instance_state' in data.keys():
    #     del data['_sa_instance_state']
    try:
        del data['_sa_instance_state']
    except:
        pass
    return list(data.values())

def get_columns(element):
    data = element.__dict__
    try:
        del data['_sa_instance_state']
    except:
        pass
    return data.keys()


def get_entity_to_dataframe(entity)->pd.DataFrame:
    conn = SessionLocal()
    items = conn.query(entity).all()
    extract_element(items[0])
    data = [extract_element(item) for item in items]
    columns = get_columns(items[0])
    conn.close()
    return pd.DataFrame(data,columns=columns)

def get_assignments()->pd.DataFrame:
    return get_entity_to_dataframe(Assignment)
    

def get_professors()->pd.DataFrame:
    return get_entity_to_dataframe(Professor)


def get_courses()->pd.DataFrame:
    return get_entity_to_dataframe(Course)


def get_classrooms()->pd.DataFrame:
    return get_entity_to_dataframe(Classroom)

def get_data()->pd.DataFrame:
    assignments = get_assignments()
    classrooms = get_classrooms()
    courses = get_courses()
    professors = get_professors()
    return assignments,classrooms,courses,professors