"""
Creates the 'assignments' table in 'university.db' with foreign keys to 'students' and 'auditorium'.
Defines relationships between student assignments and auditorium locations.
"""
import sqlite3

conn = sqlite3.connect('university.db')
c = conn.cursor()

print("Connected to database")

c.execute('''
          CREATE TABLE IF NOT EXISTS assignments (
          id_assignment INTEGER PRIMARY KEY,
          id_student INTEGER,
          id_auditorium INTEGER,
          FOREIGN KEY (id_student) REFERENCES students(id_student),
          FOREIGN KEY (id_auditorium) REFERENCES auditorium(id_auditorium)
          )
          ''')

conn.commit()

print("Changes applied. New table created and foreign key associated")

conn.close()
