import pandas as pd
import datetime
from app.db.database import excute_query,SessionLocal
from app.db.models import (
    Assignment,Professor,Classroom,CapacibilityProfessor,Course)
from sqlalchemy.orm import aliased
from datetime import time
from sqlalchemy import asc

from app.scripts.common import get_course_model

class Schedule:

    def __init__(self,professors:pd.DataFrame,assignments:pd.DataFrame,courses:pd.DataFrame,classrooms:pd.DataFrame):
        self.professors = professors
        self.assignments = assignments
        self.courses = courses
        self.classrooms = classrooms
        self.DATE_START = datetime.time(12,50,0)
        self.DATE_END   = datetime.time(22,0,0)
        self.DURATION = 50

    def get_classroom(self,capacity)->Classroom | None:
        db = SessionLocal()
        resp = db.query(Classroom).filter(
            Classroom.Capacity >= int(capacity)
        ).order_by(asc(Classroom.Capacity)).all()
        db.close()
        return resp
        
    def get_professors(self,start_hour:time,end_hour:time,course)->CapacibilityProfessor | None:
        course = int(course)
        db = SessionLocal()
        result =  db.query(CapacibilityProfessor).join(
            Professor,
            Professor.Cui == CapacibilityProfessor.Id_professor
        ).filter(
            CapacibilityProfessor.Id_course == course,
            Professor.Hour_start <= end_hour,
            Professor.Hour_end >= start_hour
        ).all()
        db.close()
        return result
    
    def get_valid_professor(self,professors,schedule,start_hour,end_hour,index=0):
        for i in range(index,len(professors)):
            professor:Professor = professors[i]
            filter = (
                ((schedule["Hora Inicio"] == start_hour) &
                (schedule["Hora Final"] == end_hour.time()) &
                (schedule["Maestro"] == professor.Id_professor))
            )
            if schedule[filter].shape[0] > 0:
                continue
            return professor,i
        return None,None
        
    def get_valid_classroom(self,classrooms,schedule,start_hour,end_hour,index=0):
        for i in range(index,len(classrooms)):
            classroom:Classroom = classrooms[i]
            filter = (
                (schedule["Salon"] == classroom.Id)  &
                (schedule["Hora Inicio"] == start_hour) &
                (schedule["Hora Final"] == end_hour.time())
            )
            if schedule[filter].shape[0] > 0:
                continue
            return classroom,i
        return None,None
    
    def fill_random_courses_by_classroom(self,assignments:pd.DataFrame,start_hour,schedule:pd.DataFrame,batch_size):
        tmp = schedule.copy(deep=True)
        data_loaded = []
        semester_loaded = []

        for i in range(0, len(assignments), batch_size):
            df_tmp = assignments.iloc[i:i + batch_size]
            end_hour = datetime.datetime.combine(datetime.datetime.min, start_hour) + datetime.timedelta(minutes=self.DURATION)
            for assign in df_tmp.values:
                course,section,total = assign

                classrooms = self.get_classroom(total)
                professors = self.get_professors(start_hour,end_hour.time() ,course)

                coursemodel = get_course_model(course_id=int(course))

                if [int(coursemodel.semester),start_hour] in semester_loaded:
                    continue
                
                if len(classrooms)>0:
                    classroom,index = self.get_valid_classroom(classrooms,schedule,start_hour,end_hour,0)
                    if classroom:
                        new_row = {
                            "Salon": classroom.Id,
                            "Hora Inicio": start_hour,
                            "Hora Final": end_hour.time(),
                            "Maestro": None,
                            "Curso": course,
                            "Sección": section,
                            "Total": total
                        }
                        schedule.loc[len(schedule)] = new_row
                        data_loaded.append([course,section])
                        semester_loaded.append([int(coursemodel.semester),start_hour])
                
                if len(professors) > 0:
                    professor,index = self.get_valid_professor(professors,schedule,start_hour,end_hour,0)
                    if professor:
                        new_row = {
                            "Salon": None,
                            "Hora Inicio": start_hour,
                            "Hora Final": end_hour.time(),
                            "Maestro": professor.Id_professor,
                            "Curso": course,
                            "Sección": section,
                            "Total": total
                        }
                        schedule.loc[len(schedule)] = new_row
                        data_loaded.append([course,section])
                        semester_loaded.append([int(coursemodel.semester),start_hour])
                


            start_hour = end_hour.time()
        filtered_df2 = pd.DataFrame(columns=['Id_course', 'Id_section', 'Total'])
        for index, row in assignments.iterrows():
            if not([row['Id_course'], row['Id_section']] in data_loaded):
                filtered_df2.loc[len(filtered_df2)] = row
        return schedule,filtered_df2

    def init(self,order=None)->pd.DataFrame:
        
        assignments = self.assignments.copy(deep=True)
        classrooms = self.classrooms.copy(deep=True)

        schedule = pd.DataFrame(data=[],columns=["Salon","Hora Inicio", "Hora Final", "Maestro", "Curso", "Sección","Total"])
        assignments = self.assignments.groupby(['Id_course', 'Id_section']).count().reset_index()
        assignments.rename(columns={'Id_student': 'Total'}, inplace=True)
        assignments = assignments.sort_values(by=['Id_course', 'Id_section'])
        
        total = classrooms["Id"].count()
        start_hour = self.DATE_START
        return self.generate_schedule(assignments,schedule,start_hour,total,order)


    def generate_schedule(self)->pd.DataFrame:
        pass