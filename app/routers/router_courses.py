from app.db.response_models import CourseModel,Schedule as ScheduleResponse
from fastapi import APIRouter,Depends,status 
from typing import List

from app.repository.repository_courses import (
    repository_delete_course, repository_get_all, repository_save_course,
    repository_get_courses_by_student
)

router = APIRouter(
    prefix="",
    tags=["Courses"]
)


"""Endpoints for courses CRUD"""
@router.get('/',response_model=List[CourseModel])
def get_courses():
    "Get all courses"
    return repository_get_all()

@router.get('/{id}',response_model=List[CourseModel])
def get_courses_by_student(id:int):
    "Get all courses by student"
    return repository_get_courses_by_student(id)

@router.post('/',response_model=CourseModel,status_code=status.HTTP_201_CREATED)
def save_course(body:CourseModel):
    "Save a new course"
    return repository_save_course(body)

@router.put('/',response_model=CourseModel,status_code=status.HTTP_201_CREATED)
def update_course(body:CourseModel):
    "Update a course info"
    return repository_save_course(body)

@router.delete('/',response_model=CourseModel,status_code=status.HTTP_200_OK)
def delete_course(body:CourseModel):
    "Delete a course"
    return repository_delete_course(body)
