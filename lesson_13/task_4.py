"""
Queries the 'books' table in 'library.db' for books written by 'A Sapkowski'.
Displays the matching records.
"""
import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

print("Connected to database")

c.execute(
    "SELECT * FROM books WHERE author = ?",
    ('A Sapkowski',)) #has to be ',' within the tuple!
fav_books = c.fetchall()
print("Favorite book:")
for book in fav_books:
    print(book)

conn.close()
