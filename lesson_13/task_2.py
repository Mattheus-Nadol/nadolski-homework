"""
Inserts a predefined list of books into the 'books' table in 'library.db'.
Each book includes title, author, and year_published.
"""
import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

print("Connected to database")

books_to_add = [
    ("Harry Potter", "JK Rowling", 1999),
    ("Lord of the Rings", "J Tolkien", 2000),
    ("The Witcher", "A Sapkowski", 2001)
]

c.executemany(
    "INSERT INTO books (title, author, year_published) VALUES (?, ?, ?)",
    books_to_add)

conn.commit()

print("Changes applied")
print(f"Added {c.rowcount * len(books_to_add)} records to the table 'books'")

conn.close()
