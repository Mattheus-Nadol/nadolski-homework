"""
Moduł: FakeClient
Symuluje klienta wysyłającego żądania do serwera.
"""

from typing import Dict, Any
from server import FakeServer

class FakeClient:
    """
    Klasa FakeClient symuluje klienta, który wysyła żądania do serwera.
    """

    def send(self, server: FakeServer, request: Dict[str, Any]) -> None:
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
