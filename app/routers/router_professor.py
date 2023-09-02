from app.db.response_models import ProfessorModel
from fastapi import APIRouter,Depends,status 
from typing import List

from app.repository.repository_professor import *

router = APIRouter(
    prefix="",
    tags=["professor"]
)

"""Endpoints for professors CRUD"""
@router.get('/',response_model=List[ProfessorModel])
def get_professors():
    return repository_get_all()

@router.get('/{cui}',response_model=List[CapacibilityProfessorModel])
def get_professors(cui:int):
    return repository_get_assigments(cui)

@router.post('/',response_model=ProfessorModel,status_code=status.HTTP_201_CREATED)
def save_professor(body:ProfessorModel):
    return repository_save_professor(body)

@router.post('/assignment',response_model=CapacibilityProfessorModel,status_code=status.HTTP_201_CREATED)
def save_assignment(body:CapacibilityProfessorModel):
    return repository_add_assignment(body)

@router.delete('/assignment',response_model=CapacibilityProfessorModel,status_code=status.HTTP_200_OK)
def remove_assignment(body:CapacibilityProfessorModel):
    return repository_remove_assignment(body)

@router.put('/',response_model=ProfessorModel,status_code=status.HTTP_201_CREATED)
def update_professor(body:ProfessorModel):
    return repository_save_professor(body)

@router.delete('/',response_model=ProfessorModel,status_code=status.HTTP_200_OK)
def delete_professor(body:ProfessorModel):
    return repository_delete_professor(body)