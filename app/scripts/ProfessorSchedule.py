from app.scripts.Schedule import Schedule
import pandas as pd
import datetime
from app.scripts.common import get_classroom_model, get_professor_model, get_section_model,get_course_model
from app.scripts.extract import get_entity_to_dataframe
from app.db.models import CapacibilityProfessor
import numpy as np
from app.db.response_models import (
    Classroom as ClassroomModel, Schedule as ScheduleModel,
    CourseModel,ProfessorModel,SectionModel
)

class ProfessorSchedule(Schedule):

    def generate_matrix(self)->pd.DataFrame:
        columns = ["Hora Inicio","Hora Fin"]
        start = self.DATE_START
        data = []
        while start < self.DATE_END:
            end = datetime.datetime.combine(datetime.datetime.min, start) + datetime.timedelta(minutes=self.DURATION)
            data.append([start,end.time()])
            start = end.time()
        df = pd.DataFrame(data=data,columns=columns)
        df_2 = df.copy(deep=True)

        for row in self.classrooms.values:
            id,name,total = row
            df[id] = int(total)
            df_2[id] = None
        return df,df_2
    
    def get_coordinates(self,spaces:pd.DataFrame,schedule:pd.DataFrame,id_professor,professor_registered):
        try:

            """Obtener los indicies o coordenadas"""
            min_index_flat = np.nanargmin(spaces.values)
            min_row = min_index_flat // spaces.shape[1]
            min_col = min_index_flat % spaces.shape[1]

            index_array = spaces.index.to_numpy()
            tmp_row = index_array[min_row]

            """Registrar espacio"""
            val1 = schedule.iat[tmp_row,0]
            val2 = schedule.iat[tmp_row,1]

            if [val1,val2,id_professor] in professor_registered:
                spaces.iat[min_row,min_col] = np.nan
                return self.get_coordinates(spaces,schedule,id_professor,professor_registered)
            else:

                return index_array[min_row],min_col
        except:
            return None,None
        
    def generate(self,assignments,schedule,batch_size,order):
        assig_professors = get_entity_to_dataframe(CapacibilityProfessor)
        
        schedule,real_schedule = self.generate_matrix()
        
        assig_professors = assig_professors.merge(self.professors, how="inner",
                               right_on='Cui',
                               left_on='Id_professor'
                               )
        
        assig_professors = assig_professors.merge(assignments,how="inner",
                                right_on='Id_course',left_on='Id_course')
        
        order_row = {
            "5":"flag",
            "2":"Hour_start",
            "3":"Id_course",
            "4":"Total",
        }
        
        
        data_loaded = []
        semester_loaded = []
        professor_registered = []
        assig_professors = assig_professors.assign(registered=False)

        cols = self.classrooms["Id"].values
        if not order == "5":
            assig_professors.sort_values(['flag',order_row[order]],ascending=[True,True],inplace=True)
        
        for index, row in assig_professors.iterrows():

            id_professor = row["Id_professor"]
            id_course = row["Id_course"]
            start_p = row["Hour_start"]
            end_p = row["Hour_end"]
            section = row["Id_section"]
            total = row["Total"]

            semester = self.courses[(self.courses["Id"] == id_course)]["Semester"]

            if [id_course,section] in data_loaded:
                continue

            filter = ( (schedule["Hora Inicio"] >= start_p) & (schedule["Hora Fin"] <= end_p))
            spaces:pd.DataFrame = schedule[filter]

            if spaces.shape[0]<=0:
                continue

            """Obtener los espacios ya filtrados y filtrar en base a la capacidad de los salones"""
            filter = (spaces[cols] >= total)
            spaces = spaces[filter]

            if spaces.shape[0]<=0:
                continue

            min_row,min_col = self.get_coordinates(spaces.copy(deep=True),schedule,id_professor,professor_registered)
            if min_row is None:
                continue

            if [int(semester),min_row] in semester_loaded:
                continue

            real_schedule.iat[min_row, min_col] = {
                            "Salon": schedule.columns[min_col],
                            "Maestro": id_professor,
                            "Curso": id_course,
                            "Sección": section,
                            "Total": total
                        }
            
            schedule.iat[min_row,min_col] = np.nan
            data_loaded.append([id_course,section])
            professor_registered.append([schedule.iat[min_row,0],schedule.iat[min_row,1],id_professor])
            
            filter = (
                (assig_professors["Id_course"] == id_course) & (assig_professors["Id_section"] == section)
            )
            assig_professors.loc[filter,"registered"] = True

            semester_loaded.append([int(semester),min_row])

        filter = ( assig_professors["registered"] == False)
        return real_schedule,assig_professors[filter],schedule

    def fill_random_courses(self,real_schedule:pd.DataFrame,extra:pd.DataFrame,schedule: pd.DataFrame):
        cols = self.classrooms["Id"].values
        data_loaded = []
        semester_loaded = []

        for index, row in extra.iterrows():
            id_professor = row["Id_professor"]
            id_course = row["Id_course"]
            start_p = row["Hour_start"]
            end_p = row["Hour_end"]
            section = row["Id_section"]
            total = row["Total"]

            semester = self.courses[(self.courses["Id"] == id_course)]["Semester"]
            
            if [id_course,section] in data_loaded:
                continue

            filter = ( (schedule["Hora Inicio"] >= start_p) & (schedule["Hora Fin"] <= end_p))
            spaces:pd.DataFrame = schedule[filter]
            if spaces.shape[0]<=0:
                continue

            """Obtener los espacios ya filtrados y filtrar en base a la capacidad de los salones"""
            filter = (spaces[cols] >= total)
            spaces = spaces[filter]
            if spaces.shape[0]<=0:
                continue

            min_row,min_col = self.get_coordinates(spaces.copy(deep=True),schedule,id_professor,[])
            if min_row is None:
                continue

            if [int(semester),min_row] in semester_loaded:
                continue

            real_schedule.iat[min_row, min_col] = {
                            "Salon": schedule.columns[min_col],
                            "Maestro": None,
                            "Curso": id_course,
                            "Sección": section,
                            "Total": total
                        }
            
            schedule.iat[min_row,min_col] = np.nan
            data_loaded.append([id_course,section])

            filter = (
                (extra["Id_course"] == id_course) & (extra["Id_section"] == section)
            )
            extra.loc[filter,"registered"] = True
            semester_loaded.append([int(semester),min_row])

        filter = ( extra["registered"] == False)

        not_loaded = []
        for index, row in extra[filter].iterrows():
            id_professor = row["Id_professor"]
            id_course = row["Id_course"]
            start_p = row["Hour_start"]
            end_p = row["Hour_end"]
            section = row["Id_section"]
            total = row["Total"]

            model = ScheduleModel(
                        classroom=None,
                        start_hour=start_p,
                        end_hour=end_p,
                        professor=get_professor_model(id_professor),
                        seccion=get_section_model(section),
                        course=get_course_model(id_course),
                        total=total,
                    )
            not_loaded.append(model)
            
        return not_loaded

    def generate_schedule(self,assignments,schedule,start_hour,total,order=None):
        df,df2,df3 = self.generate(
            assignments=assignments,schedule=schedule,batch_size=total,order=order
        )

        df2.reset_index(drop=True,inplace=True)
        not_loaded=self.fill_random_courses(df,df2,df3)

        response = []
        for row in df.values:
            end_hour = row[1]
            start_hour = row[0]
            
            schedules = []
            for cell in row[2:]:
                if cell:
                    classroom = get_classroom_model(cell["Salon"])
                    professor = get_professor_model(cell["Maestro"])
                    section = get_section_model(cell["Sección"])
                    course = get_course_model(cell["Curso"])

                    model = ScheduleModel(
                        classroom=classroom,
                        start_hour=start_hour,
                        end_hour=end_hour,
                        professor=professor,
                        seccion=section,
                        course=course,
                        total=cell["Total"],
                    )
                    schedules.append(model)
            
            response.append(schedules)
        response[-1].extend(not_loaded)
        return response
