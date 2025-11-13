"""
Zadanie 10 – Prosta symulacja ORM
Stwórz klasę Produkt w Pythonie z atrybutami id_produktu, nazwa_produktu i cena.
Następnie napisz funkcję pobierz_wszystkie_produkty(), która połączy się z bazą danych,
pobierze wszystkie produkty i zwróci listę obiektów klasy Produkt. To ćwiczenie pokaże Ci,
jak ORM automatyzuje mapowanie wierszy na obiekty.
"""
import sqlite3

class Produkt:
    """Reprezentuje produkt z bazy danych z ID, nazwą i ceną."""
    def __init__(self, id_produktu, nazwa_produktu, cena):
        self.id_produktu = id_produktu
        self.nazwa_produktu = nazwa_produktu
        self.cena = cena

def pobierz_wszystkie_produkty():
    """Pobiera wszystkie produkty z bazy danych i zwraca je jako obiekty klasy Produkt."""
    # Połączenie z bazą danych
    conn = sqlite3.connect('sklep.db')
    c = conn.cursor()
    print("✅Połączono z bazą danych!")

    # Pobranie danych z tabeli Produkty
    c.execute("""
    SELECT * 
    FROM Produkty
    """)
    product_list = []
    result = c.fetchall()
    for row in result:
        current_product = Produkt(row[0], row[1], row[2])
        product_list.append(current_product)

    # Zamykamy połączenie
    conn.close()
    # Zwrócenie listy obiektów klasy Produkt
    print("📂Produkty:")
    for product in product_list:
        print(f"OBIEKT: {product}", end=" | ")
        print(f"{product.id_produktu}. '{product.nazwa_produktu}', {product.cena:.2f} PLN")

pobierz_wszystkie_produkty()
