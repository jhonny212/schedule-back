from pydantic import BaseModel
from typing import Optional
import datetime
from typing import List
from fastapi import  UploadFile

class Classroom(BaseModel):
    id: Optional[int]
    name: Optional[str]
    capacity: Optional[int]

class AssigmentModel(BaseModel):
    id_course: int
    id_student: int
    section: int

class ProfessorModel(BaseModel):
    cui: int
    name: str
    hour_start: Optional[datetime.time]
    hour_end: Optional[datetime.time]

class CareerModel(BaseModel):
    code: int
    name: str
    extension: Optional[int]

class CourseModel(BaseModel):
    id: int
    semester: int
    name: str
    id_career: Optional[int] | None

class SectionModel(BaseModel):
    id: int
    name: str

class Schedule(BaseModel):
    classroom: Classroom | None
    start_hour: datetime.time
    end_hour: datetime.time
    professor: ProfessorModel | None
    seccion: SectionModel
    course: CourseModel
    total: int

class CapacibilityProfessorModel(BaseModel):
    
    course: CourseModel
    professor: ProfessorModel
    flag : bool

class StudentModel(BaseModel):
    carnet: int
    career: CareerModel
    name: str
    semester: Optional[int]


class ColumnModel(BaseModel):
    name: str
    primary: str
    foreign: str
    type: str

class SquemaModel(BaseModel):
    table: str
    columns: List[ColumnModel]

class FileModel(BaseModel):
    table: str
    file: UploadFile