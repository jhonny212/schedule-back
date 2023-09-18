from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.db.database import Base

class Career(Base):
    __tablename__ = 'Career'
    
    Code = Column(Integer, primary_key=True, autoincrement=True)
    Extension = Column(Integer, nullable=False)
    Name = Column(String, nullable=False)

class Student(Base):
    __tablename__ = 'Student'
    
    Carnet = Column(Integer, primary_key=True, autoincrement=True)
    Id_career = Column(Integer, ForeignKey('Career.Code'), nullable=False)
    Semester = Column(Integer, nullable=False)
    Name = Column(String, nullable=False)
    career = relationship("Career")

class CareerCourse(Base):
    __tablename__ = 'CareerCourse'
    
    Id_career = Column(Integer, ForeignKey('Career.Code'), primary_key=True)
    Id_course = Column(Integer, ForeignKey('Course.Id'), primary_key=True)

class Course(Base):
    __tablename__ = 'Course'
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Semester = Column(Integer, nullable=False)
    Name = Column(String, nullable=False)

class Section(Base):
    __tablename__ = 'Section'
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)

class SectionClassroom(Base):
    __tablename__ = 'SectionClassroom'
    
    Id_section = Column(Integer, ForeignKey('Section.Id'), primary_key=True)
    Id_classroom = Column(Integer, ForeignKey('Classroom.Id'), primary_key=True)
    Hour_start = Column(Time, nullable=False)
    Hour_end = Column(Time, nullable=False)

class Assignment(Base):
    __tablename__ = 'Assignment'
    
    Id_section = Column(Integer, ForeignKey('Section.Id'), primary_key=True)
    Id_course = Column(Integer, ForeignKey('Course.Id'), primary_key=True)
    Id_student = Column(Integer, ForeignKey('Student.Carnet'), primary_key=True)
    course = relationship("Course")

class Classroom(Base):
    __tablename__ = 'Classroom'
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Capacity = Column(Integer, nullable=False)

class Professor(Base):
    __tablename__ = 'Professor'
    
    Cui = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    Hour_start = Column(Time, nullable=False)
    Hour_end = Column(Time, nullable=False)

class CapacibilityProfessor(Base):
    __tablename__ = 'CapacibilityProfessor'
    
    Id_course = Column(Integer, ForeignKey('Course.Id'), primary_key=True)
    Id_professor = Column(Integer, ForeignKey('Professor.Cui'), primary_key=True)
    flag = Column(Boolean, nullable=False)