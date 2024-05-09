from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    mail = Column(String(50))
    pwd = Column(String(20))

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

# relationship table.
class StudentCourse(Base):
    __tablename__ = "StudentCourse"
    # id = Column(Integer, primary_key=True)
    # name = Column(String(50))
