"""
Docstring for lekcja_27.project_lesson_27.lesson_27.middleware
"""

class HTTPMethodMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Jednorazowa konfiguracja i inicjalizacja
    def __call__(self, request):
        # Kod, który zostanie wykonany dla każdego zapytania
        # zanim zostanie ono przekazane do widoku (i kolejnych middleware)
        print(f"Przetwarzam zapytanie do ścieżki: {request.path}")
        response = self.get_response(request)
        # Kod, który zostanie wykonany po przetworzeniu zapytania przez widok
        # dla każdej odpowiedzi
        print(f"Otrzymano zapytanie metodą GET: {response.status_code}")
        return response
