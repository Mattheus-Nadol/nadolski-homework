"""
Inserts sample data into 'students' and 'auditorium' tables in 'university.db'.
Displays all inserted records from both tables.
"""
import sqlite3

conn = sqlite3.connect('university.db')
c = conn.cursor()

print("Connected to database")

students_to_add = [
    ("Mateusz", "Nadolski"),
    ("Maria", "Nowak"),
    ("Łukasz", "Bobek"),
    ("Katarzyna", "Wizner")
]

auditorium_to_add = [
    ("Main_B", "C-01"),
    ("Main_A", "A-12"),
    ("Small_F", "Z-202")
]

c.executemany(
    "INSERT INTO students (name, surname) VALUES (?, ?)",
    students_to_add)

c.executemany(
    "INSERT INTO auditorium (building_name, class_number) VALUES (?, ?)",
    auditorium_to_add)

conn.commit()

print("Changes applied")
print(f"Added {c.rowcount * len(students_to_add)} records to the table 'students'")
print(f"Added {c.rowcount * len(auditorium_to_add)} records to the table 'auditorium'")

c.execute("SELECT * FROM students")
all_students = c.fetchall()
print("All students:")
for student in all_students:
    print(student)

c.execute("SELECT * FROM auditorium")
all_auditoriums = c.fetchall()
print("All auditoriums:")
for auditorium in all_auditoriums:
    print(auditorium)

conn.close()
