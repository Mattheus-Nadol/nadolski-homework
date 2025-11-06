"""
Module: student_classroom_finder

This module provides functionality to connect to a university database and retrieve
information about the classrooms assigned to students based on their surname.
It demonstrates the use of SQL JOIN operations in Python using the sqlite3 module.
"""
import sqlite3


def find_students_classroom(surname: str) -> None:
    """
    Retrieves and prints classroom assignments for a student based on surname.
    Connects to the 'university.db' database and uses SQL JOINs.
    """
    conn = sqlite3.connect('university.db')
    c = conn.cursor()

    print("Connected to database")

    c.execute("""
        SELECT students.surname, auditorium.building_name, auditorium.class_number
        FROM students
        JOIN assignments ON students.id_student = assignments.id_student
        JOIN auditorium ON assignments.id_auditorium = auditorium.id_auditorium
        WHERE students.surname = ?
              """,
              (surname,)
              )
    student_data = c.fetchall()
    if not student_data:
        print(f"Error finding the student: '{surname}'")
    else:
        for students_surname, building, classroom in student_data:
            print("Surname:", students_surname)
            print("Building:", building)
            print("Class:", classroom)
            print("---")
    conn.close()

find_students_classroom("Nadolski")
