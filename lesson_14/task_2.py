"""
Zadanie 2 – Najdroższy produkt
Napisz skrypt, który znajdzie nazwę i cenę najdroższego produktu w sklepie. Użyj funkcji
MAX().
"""
import sqlite3

conn = sqlite3.connect('sklep.db')
c = conn.cursor()
print("✅Połączono z bazą danych!")

query = """
SELECT
    nazwa_produktu,
    MAX(cena)
FROM Produkty
"""
c.execute(query)
result = c.fetchone()
print(f"Najdroższy produkt w sklepie: {result[0]}, cena: {result[1]} PLN")

# Na koniec ZAWSZE zamykamy połączenie
conn.close()