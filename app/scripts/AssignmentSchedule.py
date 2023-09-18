
from app.scripts.Schedule import Schedule
import pandas as pd
import datetime

from app.scripts.common import get_course_model

class AssignmentsSchedule(Schedule):


    def generate(self,assignments,schedule,batch_size):
        data_loaded = []
        semester_loaded = []

        """Iterar por bloques en base a la cantidad de salones"""
        for i in range(0, len(assignments), batch_size):

            start_hour = self.DATE_START

            while start_hour < self.DATE_END:
                #Obtener df y hora final
                df_tmp = assignments.iloc[i:i + batch_size]
                end_hour = datetime.datetime.combine(datetime.datetime.min, start_hour) + datetime.timedelta(minutes=self.DURATION)
                
                
                for assign in df_tmp.values:
                    course,section,total = assign

                    #Obtener profesores disponibles
                    professors = self.get_professors(start_hour,end_hour.time() ,course)
                    if len(professors)<= 0:
                        continue

                    cours = get_course_model(course_id=int(course))
                    career = int(self.career[( self.career["Id_course"] == int(course) )]["Id_career"])
                    if [int(cours.semester),start_hour,career] in semester_loaded:
                        continue
                    
                    #Obtener profesor en horario disponible
                    professor,index = self.get_valid_professor(professors,schedule,start_hour,end_hour,0)
                    if professor:
                        classrooms = self.get_classroom(total)
                        if len(classrooms)<=0:
                            continue

                        #Obtener aulas en horario disponible
                        classroom,index = self.get_valid_classroom(classrooms,schedule,start_hour,end_hour,0)
                        filter = (
                                (schedule["Curso"] == course) &
                                (schedule["Sección"] == section)
                        )
                        registered = schedule[filter].shape[0] > 0
                        

                        if classroom and not registered:
                            new_row = {
                                "Salon": classroom.Id,
                                "Hora Inicio": start_hour,
                                "Hora Final": end_hour.time(),
                                "Maestro": professor.Id_professor,
                                "Curso": professor.Id_course,
                                "Sección": section,
                                "Total": total
                            }
                            semester_loaded.append([int(cours.semester),start_hour,career])
                            schedule.loc[len(schedule)] = new_row
                            data_loaded.append([professor.Id_course,section])
                start_hour = end_hour.time()
            
        
        filtered_df2 = pd.DataFrame(columns=['Id_course', 'Id_section', 'Total'])
        for index, row in assignments.iterrows():
            if not([row['Id_course'], row['Id_section']] in data_loaded):
                filtered_df2.loc[len(filtered_df2)] = row
        
        
        return schedule,filtered_df2
    
    def generate_schedule(self,assignments,schedule,start_hour,total,order=None):
        schedule,data = self.generate(
            assignments=assignments,schedule=schedule,batch_size=total
        )
        schedule,not_loaded = self.fill_random_courses_by_classroom(assignments=data,
                                                     start_hour=start_hour,schedule=schedule,
                                                     batch_size=total)
        return schedule