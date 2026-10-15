
from database import connect_db, create_table


def add_student():
    name = input("Enter student name: ").strip()
    department = input("Enter department: ").strip()

    if not name or not department:
        print("Name and department are required.")
        return

    try:
        age = int(input("Enter age: "))
        marks = float(input("Enter marks (0-100): "))

        if age <= 0 or not 0 <= marks <= 100:
            print("Invalid age or marks.")
            return

        with connect_db() as con:
            con.execute(
                """INSERT INTO students
                   (name, age, department, marks)
                   VALUES (?, ?, ?, ?)""",
                (name, age, department, marks)
            )

        print("Student added successfully!")

    except ValueError:
        print("Please enter valid numbers.")


def view_students():
    with connect_db() as con:
        students = con.execute(
            "SELECT * FROM students ORDER BY student_id"
        ).fetchall()

    if not students:
        print("No student records found.")
        return

    for student in students:
        print(student)


def search_student():
    try:
        student_id = int(input("Enter student ID: "))

        with connect_db() as con:
            student = con.execute(
                "SELECT * FROM students WHERE student_id = ?",
                (student_id,)
            ).fetchone()

        print(student if student else "Student not found.")

    except ValueError:
        print("Enter a valid student ID.")


def update_student():
    try:
        student_id = int(input("Enter student ID to update: "))
        name = input("Enter new name: ").strip()
        department = input("Enter new department: ").strip()
        age = int(input("Enter new age: "))
        marks = float(input("Enter new marks: "))

        if not name or not department or age <= 0:
            print("Invalid student details.")
            return

        if not 0 <= marks <= 100:
            print("Marks must be between 0 and 100.")
            return

        with connect_db() as con:
            cursor = con.execute(
                """UPDATE students
                   SET name = ?, age = ?, department = ?, marks = ?
                   WHERE student_id = ?""",
                (name, age, department, marks, student_id)
            )

        print("Student updated." if cursor.rowcount
              else "Student not found.")

    except ValueError:
        print("Please enter valid numbers.")


def delete_student():
    try:
        student_id = int(input("Enter student ID to delete: "))

        with connect_db() as con:
            cursor = con.execute(
                "DELETE FROM students WHERE student_id = ?",
                (student_id,)
            )

        print("Student deleted." if cursor.rowcount
              else "Student not found.")

    except ValueError:
        print("Enter a valid student ID.")


def show_grades():
    with connect_db() as con:
        students = con.execute(
            """SELECT name, marks,
               CASE
                   WHEN marks >= 90 THEN 'A'
                   WHEN marks >= 75 THEN 'B'
                   WHEN marks >= 60 THEN 'C'
                   WHEN marks >= 40 THEN 'D'
                   ELSE 'F'
               END AS grade
               FROM students ORDER BY marks DESC"""
        ).fetchall()

    for name, marks, grade in students:
        print(f"{name}: {marks} marks - Grade {grade}")


def main():
    create_table()

    while True:
        print("""
===== STUDENT MANAGEMENT SYSTEM =====
1. Add Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Show Grades
7. Exit
""")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            show_grades()
        elif choice == "7":
            print("Thank you!")
            break
        else:
            print("Invalid option. Choose 1-7.")


if __name__ == "__main__":
    main()
