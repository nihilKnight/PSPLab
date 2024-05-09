from connector import MysqlConnector


if __name__ == "__main__":
    MysqlConnector("sec_py_sql_user", "sEcPysq!USer", "localhost", "sec_py_sql_db")\
        .insert_student("Alice", "Alice@example.com", "pwdOfAlice")\
        .insert_student("Bob", "Bob@example.com", "pwdOfBob")

