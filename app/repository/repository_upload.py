
from app.db.database import get_entity_by_id,SessionLocal,session,engine
from app.db.models import (Classroom,Course,Professor,CapacibilityProfessor,Student,Career,Assignment)
from sqlalchemy.orm import joinedload
from sqlalchemy import inspect
import pandas as pd
import io
from app.db.response_models import (
    SquemaModel,ColumnModel
)

def get_squema(type:int):
    if type == 1:
        return Classroom
    elif type == 2:
        return Course
    elif type == 3:
        return Professor
    elif type == 4:
        return CapacibilityProfessor
    elif type == 5:
        return Student
    elif type == 6:
        return Career
    elif type == 7:
        return Assignment

def repository_get_definition(type:int):
    model = get_squema(type)
    inspector = inspect(model)
    cols = []
    for column in inspector.columns:
        foreign = "Si" if len(column.foreign_keys) >0 else "No"
        primary = "Si" if column.primary_key else "No"
        name = column.key
        cols.append(ColumnModel(name=name, foreign=foreign,primary=primary,type=str(column.type)))
    return SquemaModel(table=model.__tablename__,columns=cols)

async def repository_upload_file(name:str,file):
    file_contents = await file.read()
    df = pd.read_excel(io.BytesIO(file_contents),engine='openpyxl')
    df.to_sql(name,con=engine,if_exists='append',index=False)