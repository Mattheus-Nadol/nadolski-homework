"""
Fetches and displays all records from the 'books' table in 'library.db'.
Prints each book's details to the console.
"""
import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

print("Connected to database")

c.execute("SELECT * FROM books")
all_books = c.fetchall()
print("All books:")
for book in all_books:
    print(book)

conn.close()
