
import sqlite3

con = sqlite3.connect("students.db")

cursor = con.execute("SELECT * FROM students")

for row in cursor.fetchall():
    print(row)

con.close()
