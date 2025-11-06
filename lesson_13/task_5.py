"""
Updates the publishing year of books authored by 'A Sapkowski' to 2005 in 'library.db'.
Displays the updated records.
"""
import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

print("Connected to database")
new_year = 2005

c.execute(
    "UPDATE books SET year_published = ? WHERE author = ?",
    (new_year,'A Sapkowski')) #has to be ',' within the tuple!
conn.commit()
print(f"Updated publishing year for {new_year}. Changed records: {c.rowcount}")

c.execute(
    "SELECT * FROM books WHERE year_published = ?",
    (new_year,)) #has to be ',' within the tuple!

upd_books = c.fetchall()
print("Updated book:")
for book in upd_books:
    print(book)

conn.close()
