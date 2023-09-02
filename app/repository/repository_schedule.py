import pandas as pd
import datetime
from app.db.database import get_entity_by_id
from app.db.models import (
    Assignment,Professor,Classroom,Section,Course)
from sqlalchemy.orm import aliased
from datetime import time
from sqlalchemy import asc
from app.db.response_models import (
    Classroom as ClassroomModel, Schedule as ScheduleModel,
    CourseModel,ProfessorModel,SectionModel
)

from app.scripts.AssignmentSchedule import AssignmentsSchedule
from app.scripts.ProfessorSchedule import ProfessorSchedule
from app.scripts.common import get_classroom_model, get_course_model, get_professor_model, get_section_model
from app.scripts.extract import get_data



def repository_get_schedule_by_assignment():
    assignments,classrooms,courses,professors = get_data()
    schedule = AssignmentsSchedule(
        courses=courses,assignments=assignments,
        classrooms=classrooms,professors=professors
    )
    
    df = schedule.init()
    df.sort_values(by='Hora Inicio',inplace=True)
    
    response = []
    schedules = []
    time_identifier = None
    for index, row in df.iterrows():
        if time_identifier is None:
            time_identifier = row["Hora Inicio"]
        
        """Get Classroom"""
        classroom_id = row["Salon"]

        classroom = get_classroom_model(classroom_id)
        
        """Get Course"""
        course = get_course_model(int(row["Curso"]))

        """Get Professor"""
        professor_id = row["Maestro"]
        
        professor = get_professor_model(professor_id)
        """Get section"""

        section = get_section_model(row["Sección"])
        
        schedule = ScheduleModel(
            classroom=classroom,
            start_hour=row["Hora Inicio"],
            end_hour=row["Hora Final"],
            professor=professor,
            seccion=section,
            course=course,
            total=row["Total"],
        )

        if not(row["Hora Inicio"] == time_identifier):
            response.append(schedules)
            schedules = []
            time_identifier = row["Hora Inicio"]
      
        schedules.append(schedule)
    return response
    
def repository_get_schedule_by_professor(type):
    assignments,classrooms,courses,professors = get_data()
    
    schedule = ProfessorSchedule(
        courses=courses,assignments=assignments,
        classrooms=classrooms,professors=professors
    )
    return schedule.init(type)
    
    