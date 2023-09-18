import io
from fastapi import APIRouter,Depends,status, UploadFile,File
from sqlalchemy.orm import Session
from app.db.response_models import FileModel 
from app.scripts.generate_schedule import *
from typing import List
from app.repository.repository_upload import repository_get_definition,repository_upload_file
import pandas as pd

router = APIRouter(
    prefix="",
    tags=["upload"]
)

@router.get('/{type}')
def get_squema(type:int):
    "Get definition of a table"
    return repository_get_definition(type)
    
@router.post("/{table}",status_code=status.HTTP_200_OK)
async def upload_squema(file: UploadFile, table:str):
    "Upload an excel file to bulk data"
    await repository_upload_file(table,file)
    return {}