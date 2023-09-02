from fastapi import APIRouter,Depends,status 
from sqlalchemy.orm import Session 
from typing import List
from app.scripts.generate_schedule import *
from app.db.response_models import Classroom,Schedule as ScheduleResponse
from app.repository.repository_schedule import (
    repository_get_schedule_by_assignment,
    repository_get_schedule_by_professor
)
from app.repository.repository_classroom import (
    repository_get_classrooms,repository_save_classroom,
    repository_delete_classroom
)


router = APIRouter(
    prefix="",
    tags=["Users"]
)

@router.get('/schedule',response_model=List[List[ScheduleResponse]])
def get_schedule_by_assignment():
    try:
        return repository_get_schedule_by_assignment()
    except Exception as e:
        print(e)
        return [[]]
    

@router.get('/schedule/{type}',response_model=List[List[ScheduleResponse]])
def get_schedule_by_professors(type:str):
    return repository_get_schedule_by_professor(type)


"""Endpoints for classroom CRUD"""
@router.get('/classrooms',response_model=List[Classroom])
def get_classrooms():
    return repository_get_classrooms()

@router.post('/classrooms',response_model=Classroom,status_code=status.HTTP_201_CREATED)
def save_classroom(body:Classroom):
    return repository_save_classroom(body)

@router.delete('/classrooms',response_model=Classroom,status_code=status.HTTP_200_OK)
def save_classroom(body:Classroom):
    return repository_delete_classroom(body)

@router.put('/classrooms',response_model=Classroom,status_code=status.HTTP_201_CREATED)
def save_classroom(body:Classroom):
    return repository_save_classroom(body)


