select * from "Career"

select * from "CareerCourse"

select * from "Course"

insert into "CareerCourse" ("Id_career", "Id_course")
select 2,"Id" from "Course"


delete from "CareerCourse"


delete from "Student" where "Carnet" = 0
