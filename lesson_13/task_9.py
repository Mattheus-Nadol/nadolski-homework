"""
Assigns each student from the 'students' table to an auditorium from the 'auditorium' table.
Assignments are distributed cyclically and inserted into the 'assignments' table.
Displays all assignment records.
"""
import sqlite3

conn = sqlite3.connect('university.db')
c = conn.cursor()

print("Connected to database")

c.execute("SELECT * FROM students")
all_students = c.fetchall()

c.execute("SELECT * FROM auditorium")
all_auditoriums = c.fetchall()

all_assignments:list = []
for i, student in enumerate(all_students):
    auditorium = all_auditoriums[i%len(all_auditoriums)]
    all_assignments.append((student[0], auditorium[0]))

c.executemany(
    "INSERT INTO assignments (id_student, id_auditorium) VALUES (?, ?)",
    all_assignments)


conn.commit()

print("Changes applied")
print(f"Added {len(all_assignments)} records to the table 'assignments'")


c.execute("SELECT * FROM assignments")
all_assignments = c.fetchall()
print("All asignments:")
for assignment in all_assignments:
    print(assignment)

conn.close()
