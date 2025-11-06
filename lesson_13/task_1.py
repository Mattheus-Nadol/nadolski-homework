"""
Creates a SQLite database 'library.db' and defines a table 'books' with columns:
id (primary key), title, author, and year_published.
"""

import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

print("Connected to database")

c.execute('''
          CREATE TABLE IF NOT EXISTS books (
          id INTEGER PRIMARY KEY,
          title TEXT NOT NULL,
          author TEXT NOT NULL,
          year_published INTEGER
          )
          ''')

conn.commit()

print("Changes applied")

conn.close()
