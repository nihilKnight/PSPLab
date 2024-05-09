from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker

from models import Base, Student, Course

dbEngine = "mysql"
dbapi = "mysqlconnector"


class MysqlConnector:
    def __init__(self, user: str, pwd: str, host: str, dbname: str) -> None:
        self.engine = create_engine(f"{dbEngine}+{dbapi}://{user}:{pwd}@{host}/{dbname}")
        self.session = sessionmaker(self.engine)()
        # check whether the tables exist; otherwise create those tables.
        Base.metadata.create_all(self.engine, checkfirst=True)

    def insert_student(self, name: str, mail: str, pwd="unsafe_password"):
        self.session.add(Student(name=name, mail=mail, pwd=pwd))
        self.session.commit()
        return self

    def insert_course(self, name: str):
        self.session.add(Course(name=name))
        self.session.commit()
        return self

    def update_student(self, id: int):
        pass
    
    def update_course(self, id: int):
        pass

    def delete_student(self, id: int):
        pass

    def delete_course(self, id: int):
        pass

    def select_all_students(self, id: int):
        pass

    def select_all_courses(self, id: int):
        pass

    def select_student_by_id(self, id: int):
        pass

    def select_course_by_id(self, id: int):
        pass