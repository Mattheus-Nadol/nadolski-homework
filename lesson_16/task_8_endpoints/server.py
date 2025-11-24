"""
Moduł: FakeServer
Obsługuje logikę serwera i endpointy.
"""

from typing import Dict, Any

class FakeServer:
    """
    Klasa FakeServer symuluje prosty serwer z bazą danych użytkowników.
    Obsługuje żądania HTTP typu GET i POST na zasobie /users.
    """

    def __init__(self):
        """
        Inicjalizuje serwer z przykładową bazą danych użytkowników.
        Tworzy słownik self.db z kluczem "users" i listą użytkowników.
        """
        self.db = {
            "users": [
                {"id": 1, "name": "Jan"},
                {"id": 2, "name": "Anna"}
            ]
        }
        self.next_id = 3

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obsługuje żądanie HTTP w formie słownika.
        Parametry:
            request (dict): Słownik zawierający klucze:
                - method (str): Typ żądania, np. "GET" lub "POST".
                - target (str): Ścieżka zasobu, np. "/users".
                - body (dict, opcjonalnie): Dane do dodania (dla POST).
        Zwraca:
            dict: Odpowiedź z kodem statusu i danymi.
        """
        method = request.get("method")
        target = request.get("target")

        routes = {
            ("GET", "/users"): self.handle_get_users,
            ("POST", "/users"): self.handle_post_users
        }

        handler = routes.get((method, target))
        if handler:
            return handler(request)
        return {"status": 404, "body": {"error": "Not Found"}}

    def handle_get_users(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obsługuje żądanie GET /users.
        Parametry:
            request (dict): Słownik z danymi żądania (nieużywany w tej wersji).
        Zwraca:
            dict: Odpowiedź z kodem statusu i listą użytkowników.
        """
        return {"status": 200, "body": self.db["users"]}

    def handle_post_users(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obsługuje żądanie POST /users.
        Parametry:
            request (dict): Słownik z danymi żądania, zawiera klucz "body" z danymi nowego użytkownika.
        Zwraca:
            dict: Odpowiedź z kodem statusu i dodanym użytkownikiem.
        """
        body = request.get("body", {})
        new_user = {"id": self.next_id, **body}
        self.db["users"].append(new_user)
        self.next_id += 1
        return {"status": 201, "body": new_user}
