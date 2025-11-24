"""
Moduł: main
Scenariusze testowe dla interakcji klient-serwer.
"""

from server import FakeServer
from client import FakeClient

def main():
    """
    Funkcja główna uruchamia scenariusze testowe:
    - Pobranie wszystkich użytkowników
    - Dodanie nowego użytkownika
    - Ponowne pobranie użytkowników
    - Próba dostępu do nieistniejącego zasobu
    """
    my_server = FakeServer()
    my_client = FakeClient()

    # 1. Pobranie wszystkich użytkowników
    my_client.send(my_server, {"method": "GET", "target": "/users"})

    # 2. Dodanie nowego użytkownika
    my_client.send(my_server, {"method": "POST", "target": "/users", "body": {"name": "Kasia"}})

    # 3. Ponowne pobranie użytkowników
    my_client.send(my_server, {"method": "GET", "target": "/users"})

    # 4. Próba dostępu do nieistniejącego zasobu
    my_client.send(my_server, {"method": "GET", "target": "/mix"})

if __name__ == "__main__":
    main()
