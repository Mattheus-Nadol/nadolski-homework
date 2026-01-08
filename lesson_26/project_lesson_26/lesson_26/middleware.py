"""
Docstring for lekcja_26.project_lesson_26.lesson_26.middleware
"""
# (26) Zadanie 7
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
