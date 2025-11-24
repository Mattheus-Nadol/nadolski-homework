"""
Moduł: Symulacja Klient-Serwer
Ten moduł zawiera klasy FakeServer i FakeClient, które symulują prostą interakcję
klient-serwer z obsługą żądań GET i POST.
"""

from typing import Dict, Any

class FakeServer:
    """
    Klasa FakeServer symuluje serwer z prostą bazą danych użytkowników.
    Obsługuje żądania GET i POST na zasobie /users.
    """
    def __init__(self):
        """
        Inicjalizuje serwer z przykładową bazą danych użytkowników.
        Tworzy słownik self.db z kluczem "users" i listą użytkowników.
        """
        # "Baza danych" w postaci słownika
        self.db = {
            "users": [
                {"id": 1, "name": "Jan"},
                {"id": 2, "name": "Anna"}
            ]
        }
        self.next_id = 3  # do nadawania ID nowym użytkownikom

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obsługuje żądanie HTTP w formie słownika.
        
        Parametry:
            request (dict): Słownik zawierający klucze:
                - method (str): Typ żądania, np. "GET" lub "POST".
                - target (str): Ścieżka zasobu, np. "/users".
                - body (dict, opcjonalnie): Dane do dodania (dla POST).
        
        Zwraca:
            dict: Słownik odpowiedzi z kluczami:
                - status (int): Kod odpowiedzi (200, 201, 404).
                - body (Any): Dane odpowiedzi (lista użytkowników lub komunikat błędu).
        """
        method = request.get("method")
        target = request.get("target")
        body = request.get("body", {})

        # Obsługa GET /users
        if method == "GET" and target == "/users":
            return {"status": 200, "body": self.db["users"]}

        # Obsługa POST /users
        elif method == "POST" and target == "/users":
            new_user = {"id": self.next_id, **body}
            self.db["users"].append(new_user)
            self.next_id += 1
            return {"status": 201, "body": new_user}

        # Inne przypadki -> 404
        else:
            return {"status": 404, "body": {"error": "Not Found"}}


class FakeClient:
    """
    Klasa FakeClient symuluje klienta, który wysyła żądania do serwera.
    Posiada metodę send, która przekazuje żądanie do serwera i drukuje odpowiedź.
    """
    def send(self, server: FakeServer, request: dict):
        """
        Wysyła żądanie do serwera i drukuje odpowiedź.
    
        Parametry:
            server (FakeServer): Obiekt serwera, do którego wysyłamy żądanie.
            request (dict): Słownik reprezentujący żądanie HTTP.
    
        Zwraca:
            None: Metoda tylko drukuje odpowiedź.
        """
        response = server.handle_request(request)
        print(f"Request: {request}")
        print(f"Response: {response}")
        print("-" * 40)


# Testy scenariuszy
my_server = FakeServer()
my_client = FakeClient()

# 1. Pobranie wszystkich użytkowników
my_client.send(my_server, {"method": "GET", "target": "/users"})

# 2. Dodanie nowego użytkownika
my_client.send(my_server, {"method": "POST", "target": "/users", "body": {"name": "Kasia"}})

# 3. Ponowne pobranie użytkowników (sprawdzenie, czy Kasia została dodana)
my_client.send(my_server, {"method": "GET", "target": "/users"})

# 4. Próba dostępu do nieistniejącego zasobu
my_client.send(my_server, {"method": "GET", "target": "/mix"})
