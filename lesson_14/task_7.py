"""
Zadanie 7 – Zamówienia Anny Nowak
Napisz skrypt, który wyświetli nazwy wszystkich produktów zamówionych przez klienta o
imieniu 'Anna Nowak'. Będziesz potrzebować połączyć dane z czterech tabel: Klienci,
Zamowienia, Zamowienia_Produkty i Produkty.
"""
import sqlite3

conn = sqlite3.connect('sklep.db')
c = conn.cursor()
print("✅Połączono z bazą danych!")

query = """
SELECT
    Produkty.nazwa_produktu
FROM Produkty
JOIN Klienci ON Zamowienia.id_klienta = Klienci.id_klienta
JOIN Zamowienia ON Zamowienia_Produkty.id_zamowienia = Zamowienia.id_zamowienia
JOIN Zamowienia_Produkty ON Produkty.id_produktu = Zamowienia_Produkty.id_produktu
WHERE imie = 'Anna Nowak'
"""
c.execute(query)
result = c.fetchall()
print("📂Produkty Anny Nowak:")
for row in result:
    print(f"- {row[0]}")

# Na koniec ZAWSZE zamykamy połączenie
conn.close()