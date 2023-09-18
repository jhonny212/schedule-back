from fastapi import APIRouter,Depends,status 
from sqlalchemy.orm import Session 
from app.scripts.generate_schedule import *
from typing import List
from app.db.response_models import Classroom,Schedule as ScheduleResponse

from app.repository.repository_classroom import (
    repository_get_classrooms,repository_save_classroom,
    repository_delete_classroom
)


router = APIRouter(
    prefix="",
    tags=["classrooms"]
)

"""Endpoints for classroom CRUD"""
@router.get('/',response_model=List[Classroom])
def get_classrooms():
    "Get all classrooms"
    return repository_get_classrooms()

@router.post('/',response_model=Classroom,status_code=status.HTTP_201_CREATED)
def save_classroom(body:Classroom):
    "Save classroom"
    return repository_save_classroom(body)

@router.delete('/',response_model=Classroom,status_code=status.HTTP_200_OK)
def save_classroom(body:Classroom):
    "Remove a classroom"
    return repository_delete_classroom(body)

@router.put('/',response_model=Classroom,status_code=status.HTTP_201_CREATED)
def update_classroom(body:Classroom):
    "Update a classroom"
    return repository_save_classroom(body)