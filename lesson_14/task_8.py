"""
Zadanie 8 – Kategorie z liczbą produktów
Napisz zapytanie, które wyświetli nazwę każdej kategorii oraz liczbę produktów należących
do tej kategorii. Użyj JOIN, COUNT() oraz GROUP BY.
"""
import sqlite3

conn = sqlite3.connect('sklep.db')
c = conn.cursor()
print("✅Połączono z bazą danych!")

query = """
SELECT
    Kategorie.nazwa_kategorii as kategoria,
    COUNT(nazwa_produktu)
FROM Produkty
JOIN Kategorie ON Produkty.id_kategorii = Kategorie.id_kategorii
GROUP BY kategoria
"""
c.execute(query)
result = c.fetchall()
print("📂Produkty:")
for row in result:
    print(f"- Kategoria: {row[0]}, liczba produktów: {row[1]}")

# Na koniec ZAWSZE zamykamy połączenie
conn.close()