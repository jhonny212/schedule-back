from fastapi import APIRouter,Depends,status 
from sqlalchemy.orm import Session 
from app.scripts.generate_schedule import *
from typing import List
from app.db.response_models import CareerModel
from app.repository.repository_career import (
    repository_get_career_by_course,repository_get_careers
)


router = APIRouter(
    prefix="",
    tags=["career"]
)

"""Endpoints for CRUD"""


@router.get('',response_model=List[CareerModel])
def get_careers():
    "Get all careers"
    return repository_get_careers()

@router.get('/{course_id}',response_model=CareerModel|None)
def get_career_by_course(course_id:int):
    "Get career by course"
    return repository_get_career_by_course(course_id)
