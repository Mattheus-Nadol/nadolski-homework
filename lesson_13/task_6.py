"""
Creates a SQLite database 'university.db' and defines two tables:
'students' with id, name, surname;
'auditorium' with id, building_name, and class_number.
"""
import sqlite3

conn = sqlite3.connect('university.db')
c = conn.cursor()

print("Connected to database")

c.execute('''
          CREATE TABLE IF NOT EXISTS students (
          id_student INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          surname TEXT NOT NULL
          )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS auditorium (
          id_auditorium INTEGER PRIMARY KEY,
          building_name TEXT NOT NULL,
          class_number INTEGER
          )
          ''')

conn.commit()

print("Changes applied. Two tables created")

conn.close()
