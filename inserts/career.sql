INSERT INTO public."Career"
("Extension","Name") VALUES
(1,'Ingenieria Industrial'),
(2,'Ingenieria En Sistemas')
;


insert into "CareerCourse" ("Id_career", "Id_course")
select 2,"Id" from "Course"
