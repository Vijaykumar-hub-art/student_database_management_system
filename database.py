
import sqlite3

DATABASE = "students.db"


def connect_db():
    return sqlite3.connect(DATABASE)


def create_table():
    with open("schema.sql", "r", encoding="utf-8") as file:
        sql_script = file.read()

    with connect_db() as connection:
        connection.executescript(sql_script)
