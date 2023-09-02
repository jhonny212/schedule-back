from app.db.response_models import CourseModel,Schedule as ScheduleResponse
from fastapi import APIRouter,Depends,status 
from typing import List

from app.repository.repository_courses import repository_delete_course, repository_get_all, repository_save_course

router = APIRouter(
    prefix="",
    tags=["Courses"]
)


"""Endpoints for courses CRUD"""
@router.get('/',response_model=List[CourseModel])
def get_courses():
    return repository_get_all()

@router.post('/',response_model=CourseModel,status_code=status.HTTP_201_CREATED)
def save_course(body:CourseModel):
    return repository_save_course(body)

@router.put('/',response_model=CourseModel,status_code=status.HTTP_201_CREATED)
def save_classroom(body:CourseModel):
    return repository_save_course(body)

@router.delete('/',response_model=CourseModel,status_code=status.HTTP_200_OK)
def save_course(body:CourseModel):
    return repository_delete_course(body)