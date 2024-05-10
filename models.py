from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    mail = Column(String(50), unique=True)
    pwd = Column(String(20))

    def __str__(self):
        return f"Student(id={self.id}; name={self.name}; mail={self.mail}; pwd={self.pwd[:1]}***)"

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __str__(self):
        return f"Course(id={self.id}; name={self.name})"
