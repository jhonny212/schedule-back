-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "Career" (
    "Code" bigserial   NOT NULL,
    "Extension" int   NOT NULL,
    CONSTRAINT "pk_Career" PRIMARY KEY (
        "Code"
     )
);

CREATE TABLE "Student" (
    "Carnet" bigserial   NOT NULL,
    "Id_career" bigserial   NOT NULL,
    "Semester" int   NOT NULL,
    "Name" text   NOT NULL,
    CONSTRAINT "pk_Student" PRIMARY KEY (
        "Carnet"
     )
);

CREATE TABLE "CareerCourse" (
    "Id_career" bigserial   NOT NULL,
    "Id_course" bigserial   NOT NULL,
    CONSTRAINT "pk_CareerCourse" PRIMARY KEY (
        "Id_career","Id_course"
     )
);

CREATE TABLE "Course" (
    "Id" bigserial   NOT NULL,
    "Semester" int   NOT NULL,
    "Name" text   NOT NULL,
    CONSTRAINT "pk_Course" PRIMARY KEY (
        "Id"
     )
);

CREATE TABLE "Section" (
    "Id" bigserial   NOT NULL,
    "Name" text   NOT NULL,
    CONSTRAINT "pk_Section" PRIMARY KEY (
        "Id"
     )
);

CREATE TABLE "SectionClassroom" (
    "Id_section" bigserial   NOT NULL,
    "Id_classroom" bigserial   NOT NULL,
    "Hour_start" time   NOT NULL,
    "Hour_end" time   NOT NULL,
    CONSTRAINT "pk_SectionClassroom" PRIMARY KEY (
        "Id_section","Id_classroom"
     )
);

CREATE TABLE "Assignment" (
    "Id_section" bigserial   NOT NULL,
    "Id_course" bigserial   NOT NULL,
    "Id_student" bigserial   NOT NULL,
    CONSTRAINT "pk_Assignment" PRIMARY KEY (
        "Id_section","Id_course","Id_student"
     )
);

CREATE TABLE "Classroom" (
    "Id" bigserial   NOT NULL,
    "Name" text   NOT NULL,
    "Capacity" int   NOT NULL,
    CONSTRAINT "pk_Classroom" PRIMARY KEY (
        "Id"
     )
);

CREATE TABLE "Professor" (
    "Cui" bigserial   NOT NULL,
    "Name" text   NOT NULL,
    "Hour_start" time   NOT NULL,
    "Hour_end" time   NOT NULL,
    CONSTRAINT "pk_Professor" PRIMARY KEY (
        "Cui"
     )
);

CREATE TABLE "CapacibilityProfessor" (
    "Id_course" bigserial   NOT NULL,
    "Id_professor" bigserial   NOT NULL,
    "flag" bool   NOT NULL,
    CONSTRAINT "pk_CapacibilityProfessor" PRIMARY KEY (
        "Id_course","Id_professor"
     )
);

-- Free plan table limit reached. SUBSCRIBE for more.



ALTER TABLE "Student" ADD CONSTRAINT "fk_Student_Id_career" FOREIGN KEY("Id_career")
REFERENCES "Career" ("Code");

ALTER TABLE "CareerCourse" ADD CONSTRAINT "fk_CareerCourse_Id_career" FOREIGN KEY("Id_career")
REFERENCES "Career" ("Code");

ALTER TABLE "CareerCourse" ADD CONSTRAINT "fk_CareerCourse_Id_course" FOREIGN KEY("Id_course")
REFERENCES "Course" ("Id");

ALTER TABLE "SectionClassroom" ADD CONSTRAINT "fk_SectionClassroom_Id_section" FOREIGN KEY("Id_section")
REFERENCES "Section" ("Id");

ALTER TABLE "SectionClassroom" ADD CONSTRAINT "fk_SectionClassroom_Id_classroom" FOREIGN KEY("Id_classroom")
REFERENCES "Classroom" ("Id");

ALTER TABLE "Assignment" ADD CONSTRAINT "fk_Assignment_Id_section" FOREIGN KEY("Id_section")
REFERENCES "Section" ("Id");

ALTER TABLE "Assignment" ADD CONSTRAINT "fk_Assignment_Id_course" FOREIGN KEY("Id_course")
REFERENCES "Course" ("Id");

ALTER TABLE "Assignment" ADD CONSTRAINT "fk_Assignment_Id_student" FOREIGN KEY("Id_student")
REFERENCES "Student" ("Carnet");

ALTER TABLE "CapacibilityProfessor" ADD CONSTRAINT "fk_CapacibilityProfessor_Id_course" FOREIGN KEY("Id_course")
REFERENCES "Course" ("Id");

ALTER TABLE "CapacibilityProfessor" ADD CONSTRAINT "fk_CapacibilityProfessor_Id_professor" FOREIGN KEY("Id_professor")
REFERENCES "Professor" ("Cui");

-- Free plan table limit reached. SUBSCRIBE for more.



-- Free plan table limit reached. SUBSCRIBE for more.



