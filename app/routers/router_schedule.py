from fastapi import APIRouter,Depends,status 
from sqlalchemy.orm import Session 
from typing import List
from app.scripts.generate_schedule import *
from app.db.response_models import Classroom,Schedule as ScheduleResponse
from app.repository.repository_schedule import (
    repository_get_schedule_by_assignment,
    repository_get_schedule_by_professor
)


router = APIRouter(
    prefix="",
    tags=["Users"]
)

@router.get('/schedule',response_model=List[List[ScheduleResponse]])
def get_schedule_by_assignment():
    "Get schedule by assignment"
    return repository_get_schedule_by_assignment()
    

@router.get('/schedule/{type}',response_model=List[List[ScheduleResponse]])
def get_schedule_by_professors(type:str):
    "Get schedule"
    return repository_get_schedule_by_professor(type)




