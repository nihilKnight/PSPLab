from sqlalchemy import text
from connector import MysqlConnector

if __name__ == "__main__":
    try:
        msc = MysqlConnector("sec_py_sql_user", "sEcPysq!USer", "localhost", "sec_py_sql_db")
        msc.session.execute(text("SELECT 1"))
        print("\n-------------Successfully connnected.\n")
    except Exception as e:
        print("\n-------------Failed with exception:\n")
        print(e)
