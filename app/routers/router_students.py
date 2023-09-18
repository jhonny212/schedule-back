from fastapi import APIRouter,Depends,status 
from sqlalchemy.orm import Session 
from app.scripts.generate_schedule import *
from typing import List
from app.db.response_models import StudentModel,AssigmentModel

from app.repository.repository_students import (
    repository_delete_students,repository_get_studentss,repository_save_students,
    repository_remove_assignment,repository_assign_course
)


router = APIRouter(
    prefix="",
    tags=["studentss"]
)

"""Endpoints for students CRUD"""
@router.get('/',response_model=List[StudentModel])
def get_studentss():
    "Get all students"
    return repository_get_studentss()

@router.post('/',response_model=StudentModel,status_code=status.HTTP_201_CREATED)
def save_students(body:StudentModel):
    "Save a student"
    return repository_save_students(body)

@router.post('/assign',response_model=AssigmentModel,status_code=status.HTTP_201_CREATED)
def assign_students(body:AssigmentModel):
    "Assign a course to a student"
    return repository_assign_course(body)

@router.delete('/',response_model=StudentModel,status_code=status.HTTP_200_OK)
def delete_students(body:StudentModel):
    "Remove an student"
    return repository_delete_students(body)

@router.delete('/remove/{student}/{course}',status_code=status.HTTP_200_OK)
def remove_assig_students(student: int, course: int):
    "Remove assignment of a course from a student"
    return repository_remove_assignment(student,course)

@router.put('/',response_model=StudentModel,status_code=status.HTTP_201_CREATED)
def update_students(body:StudentModel):
    "Update student info"
    return repository_save_students(body)