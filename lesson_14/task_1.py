"""
Zadanie 1 – Liczba produktów
Napisz skrypt, który połączy się z bazą sklep.db i policzy, ile jest wszystkich produktów w
tabeli Produkty. Użyj funkcji COUNT()
"""
import sqlite3

conn = sqlite3.connect('sklep.db')
c = conn.cursor()
print("✅Połączono z bazą danych!")

query = """
SELECT COUNT(id_produktu) as liczba_produktow
FROM Produkty
"""
c.execute(query)
result = c.fetchone()
print(f"Liczba wszystkich produtków w tabeli Produkty to: {result[0]}")

# Na koniec ZAWSZE zamykamy połączenie
conn.close()