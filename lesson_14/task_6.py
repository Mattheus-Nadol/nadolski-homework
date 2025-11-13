"""
Zadanie 6 – Produkty droższe od średniej
Napisz skrypt, który wyświetli nazwy i ceny wszystkich produktów, 
których cena jest wyższa niż średnia cena wszystkich produktów w sklepie. 
Wykorzystaj podzapytanie.
"""
import sqlite3

conn = sqlite3.connect('sklep.db')
c = conn.cursor()
print("✅Połączono z bazą danych!")

sub_query = """
SELECT AVG(cena) FROM Produkty
"""
c.execute(sub_query)
sub_result = c.fetchone()
print(f"🏷️ Średnia cena: {sub_result[0]:.2f} PLN")

query = """
SELECT
    nazwa_produktu,
    cena
FROM Produkty
WHERE cena > (SELECT AVG(cena) FROM Produkty)
"""
c.execute(query)
result = c.fetchall()
print("📂Produkty droższe od średniej ceny:")
for row in result:
    print(f"- {row[0]}, {row[1]} PLN")

# Na koniec ZAWSZE zamykamy połączenie
conn.close()