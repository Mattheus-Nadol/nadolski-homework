"""
Zadanie 9 – Funkcja do wyszukiwania produktów
Napisz w Pythonie funkcję znajdz_produkty_w_kategorii(nazwa_kategorii), która przyjmuje
jako argument nazwę kategorii i zwraca listę krotek (nazwa_produktu, cena) dla wszystkich
produktów w tej kategorii.
"""
import sqlite3

def znajdz_produkty_w_kategorii(nazwa_kategorii: str) -> None:
    """Funkcja przyjmuje nazwę kategorii jako argument.
    Zwraca listę produtków i ich ceny w podanej kategorii"""
    conn = sqlite3.connect('sklep.db')
    c = conn.cursor()
    print("✅Połączono z bazą danych!")

    c.execute("""
    SELECT nazwa_produktu, cena 
    FROM Produkty
    JOIN Kategorie ON Produkty.id_kategorii = Kategorie.id_kategorii
    WHERE nazwa_kategorii = ?
    """,
    (nazwa_kategorii,))

    result = c.fetchall()
    print("📂Produkty z kategorii:", nazwa_kategorii)
    for row in result:
        print(f"- Produkt: {row[0]}, cena: {row[1]} PLN")

    # Na koniec ZAWSZE zamykamy połączenie
    conn.close()

znajdz_produkty_w_kategorii("Elektronika")
# [('Laptop Pro', 5200.0), ('Smartfon X', 2500.0), ('Słuchawki bezprzewodowe', 450.0)]
znajdz_produkty_w_kategorii("Dom i ogród")
# [('Kosiarka elektryczna', 750.0), ('Zestaw narzędzi', 300.0)]
znajdz_produkty_w_kategorii("Książki")
# [('Python dla każdego', 89.99), ('Wzorce projektowe', 120.5)]
