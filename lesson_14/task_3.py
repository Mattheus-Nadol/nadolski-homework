"""
Zadanie 3 – Suma wartości
Oblicz i wyświetl łączną wartość wszystkich produktów z kategorii "Elektronika".
Użyj funkcji SUM() oraz klauzuli WHERE z JOIN.
"""
import sqlite3

conn = sqlite3.connect('sklep.db')
c = conn.cursor()
print("✅Połączono z bazą danych!")

query = """
SELECT
    Kategorie.nazwa_kategorii as kategoria,
    SUM(Produkty.cena)
FROM Produkty
JOIN Kategorie ON Produkty.id_kategorii = Kategorie.id_kategorii
WHERE kategoria = 'Elektronika'
"""
c.execute(query)
result = c.fetchone()
print(f"Kategoria {result[0]}, łączna wartość: {result[1]} PLN")

# Na koniec ZAWSZE zamykamy połączenie
conn.close()