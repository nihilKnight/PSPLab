from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import sessionmaker

from models import Base, Student, Course

dbEngine = "mysql"
dbapi = "mysqlconnector"
defaultPwd = "unsafe_password"


class MysqlConnector:
    def __init__(self, user: str, pwd: str, host: str, dbname: str) -> None:
        self.engine = create_engine(f"{dbEngine}+{dbapi}://{user}:{pwd}@{host}/{dbname}")
        self.session = sessionmaker(self.engine)()
        # check whether the tables exist; otherwise create those tables.
        Base.metadata.create_all(self.engine, checkfirst=True)

    def insert_student(self, name: str, mail: str, pwd=defaultPwd):
        self.session.add(Student(name=name, mail=mail, pwd=pwd))
        self.session.commit()
        return self

    def insert_course(self, name: str):
        self.session.add(Course(name=name))
        self.session.commit()
        return self

    def update_student(self, id: int, name=None, mail=None, pwd=None):
        stmt = (update(Student).where(Student.id==id))
        if name is not None:
            stmt = stmt.values(name=name)
        if mail is not None:
            stmt = stmt.values(mail=mail)
        if pwd is not None:
            stmt = stmt.values(pwd=pwd)
        self.session.execute(stmt)
        self.session.commit()
        return self

    def update_course(self, id: int, name=None):
        stmt = (update(Course).where(Course.id==id))
        if name is not None:
            stmt = stmt.values(name=name)
        self.session.execute(stmt)
        self.session.commit()
        return self

    def delete_student_by_id(self, id: int):
        self.session.execute(delete(Student).where(Student.id==id))
        self.session.commit()
        return self

    def delete_course_by_id(self, id: int):
        self.session.execute(delete(Course).where(Course.id==id))
        self.session.commit()
        return self

    def delete_student_by_name(self, name: str):
        self.session.execute(delete(Student).where(Student.name==name))
        self.session.commit()
        return self

    def delete_course_by_name(self, name: str):
        self.session.execute(delete(Course).where(Course.name==name))
        self.session.commit()
        return self

    def select_all_students(self):
        return self.session.query(Student)

    def select_all_courses(self):
        return self.session.query(Course)

    def select_student_by_id(self, id: int):
        return self.session.query(Student).filter_by(id=id)

    def select_course_by_id(self, id: int):
        return self.session.query(Course).filter_by(id=id)

    def select_student_by_mail(self, mail: str):
        return self.session.query(Student).filter_by(mail=mail)

