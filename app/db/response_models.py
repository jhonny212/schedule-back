from pydantic import BaseModel
from typing import Optional
import datetime

class Classroom(BaseModel):
    id: Optional[int]
    name: Optional[str]
    capacity: Optional[int]

class ProfessorModel(BaseModel):
    cui: int
    name: str
    hour_start: Optional[datetime.time]
    hour_end: Optional[datetime.time]

class CourseModel(BaseModel):
    id: int
    semester: int
    name: str

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