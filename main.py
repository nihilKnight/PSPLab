from string import ascii_lowercase, digits
from random import choice, randint
from connector import MysqlConnector
from filter import filter_input

def random_name_gen(n: int):
    return ''.join(choice(ascii_lowercase + digits) for _ in range(n))

def random_mail_gen(n: int):
    return ''.join(choice(ascii_lowercase + digits) for _ in range(n)) + [".com", ".net", ".org"][randint(0,2)]

def random_pwd_gen(n: int):
    return ''.join(choice(ascii_lowercase + digits) for _ in range(n))

if __name__ == "__main__":
    msc = MysqlConnector("sec_py_sql_user", "sEcPysq!USer", "localhost", "sec_py_sql_db")\
            # .insert_student("user_"+random_name_gen(5), random_mail_gen(randint(5,10)), "pwdOfAlice")\
            # .insert_student("user_"+random_name_gen(5), random_mail_gen(randint(5,10)), "pwdOfBob")\
            # .insert_student("user_"+random_name_gen(5), random_mail_gen(randint(5,10)), "pwdOfEve")\
            # .update_student(id=1, name="David", mail="updated_"+random_mail_gen(randint(5,10)))\
            # .update_student(id=2, name="Helen", mail="updated_"+random_mail_gen(randint(5,10)))\
            # .insert_course(random_name_gen(2)+"_Mathematical Analysis")\
            # .insert_course(random_name_gen(2)+"_Adavanced Algebra")\
            # .insert_course(random_name_gen(2)+"_Python Dangerous Programming")\
            # .update_course(id=3, name=random_name_gen(2)+"_Python Security Programming")

    # students = msc.select_all_students()
    # courses = msc.select_all_courses()

    # print()
    # for stu in students:
    #     print(stu)

    # for cour in courses:
    #     print(cour)
    # print()

    while True:
        input_name = input("Please type in name of the new student: ").strip()
        input_mail = input("Please type in mail of the new student: ").strip()
        try: 
            print()
            msc.insert_student(name=filter_input(input_name), mail=filter_input(input_mail))
            students = msc.select_all_students()
            courses = msc.select_all_courses()
            for stu in students:
                print(stu)
            for cour in courses:
                print(cour)
            print()
        except ValueError:
            print(f"Invalid input: name={input_name}, mail={input_mail}")
            print()

