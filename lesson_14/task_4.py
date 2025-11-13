"""
Zadanie 4 – Średnia cena książki
Napisz zapytanie, które obliczy średnią cenę produktów w kategorii "Książki". 
Użyj AVG().
"""
import sqlite3

conn = sqlite3.connect('sklep.db')
c = conn.cursor()
print("✅Połączono z bazą danych!")

query = """
SELECT
    Kategorie.nazwa_kategorii as kategoria,
    AVG(Produkty.cena)
FROM Produkty
JOIN Kategorie ON Produkty.id_kategorii = Kategorie.id_kategorii
WHERE kategoria = 'Książki'
"""
c.execute(query)
result = c.fetchone()
print(f"Kategoria {result[0]}, średnia cena: {result[1]:.2f} PLN")

# Na koniec ZAWSZE zamykamy połączenie
conn.close()