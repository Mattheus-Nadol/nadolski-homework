"""
Zadanie 5 – Lista klientów
Napisz skrypt, który wyświetli imiona i adresy e-mail 
wszystkich klientów z tabeli Klienci.
"""
import sqlite3

conn = sqlite3.connect('sklep.db')
c = conn.cursor()
print("✅Połączono z bazą danych!")

query = """
SELECT
    imie,
    email
FROM Klienci
"""
c.execute(query)
result = c.fetchall()
print("📂Dane klientów:")
for row in result:
    print(f"- {row[0]}, {row[1]}")

# Na koniec ZAWSZE zamykamy połączenie
conn.close()