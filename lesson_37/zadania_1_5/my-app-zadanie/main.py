# Aplikacja aiohttp – obsługa zmiennej środowiskowej NAME

"""
Educyjna aplikacja webowa wykorzystująca aiohttp.

Co robi aplikacja:
- Odczytuje zmienną środowiskową NAME
- Jeśli NAME nie istnieje → używa wartości domyślnej
- Zwraca odpowiedź HTTP "Hello, {NAME}!"
"""

import os
from aiohttp import web

# (37) Zadanie 4
# Konfiguracja zapisu logów do pliku z użyciem woluminu Dockera

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Tworzymy katalog logs jeśli nie istnieje
os.makedirs(LOG_DIR, exist_ok=True)

# Pobieramy zmienną środowiskową NAME
# Jeśli nie istnieje → używamy wartości domyślnej "Docker"
NAME = os.getenv("NAME", "Docker")

async def handle(request):
    """
    Endpoint HTTP zwracający powitanie.

    Dlaczego używamy request?
    -------------------------
    aiohttp wymaga handlera przyjmującego request,
    nawet jeśli nie używamy danych z requesta.

    Logika działania:
    1. Odczytaj wartość NAME
    2. Zwróć tekst odpowiedzi
    """

    # Odczytanie zmiennej środowiskowej podczas zapytania
    # (dobra praktyka – konfiguracja może się zmieniać)
    name = os.getenv("NAME", NAME)

    # (37) Zadanie 4
    # Bezpieczny zapis logów – obsługa uprawnień plików w kontenerze
    # Użyłem blok try/except, ponieważ pokazuje odporność kodu na błędy systemu plików w kontenerze

    try:
        # Upewniamy się, że katalog logów istnieje
        os.makedirs(LOG_DIR, exist_ok=True)

        # Zapis logu w trybie append
        with open(LOG_FILE, "a") as f:
            f.write(f"Request received. NAME={name}\n")

    except PermissionError:
        # Jeśli użytkownik kontenera nie ma praw do katalogu logs,
        # próbujemy zapisać log w katalogu tymczasowym
        fallback_log = "/tmp/app.log"

        with open(fallback_log, "a") as f:
            f.write(f"Request received. NAME={name}\n")

    return web.Response(text=f"Hello, {name}!")

# Tworzymy aplikację webową
app = web.Application()
app.router.add_get("/", handle)

# Uruchomienie serwera
if __name__ == "__main__":
    # Uruchamiamy aplikację na wszystkich interfejsach kontenera.

    # host = 0.0.0.0 → pozwala na dostęp z zewnątrz kontenera
    # port = 8000 → standardowy port aplikacji

    web.run_app(app, host="0.0.0.0", port=8000)


# TESTING – Ogólne kroki (dla wszystkich zadań)

# 1. Zbuduj obraz:
#    docker build -t my-app .

# 2. Uruchom kontener:
#    docker run -p 8000:8000 --name my-app-container my-app
#    (bez podania nazwy, system wybierze losową nazwę kontenera)

# 3. Sprawdź działające kontenery:
#    docker ps -a

# 4. Sprawdź logi kontenera:
#    docker logs my-app-container

# ------------------------------------------------------------

# TESTING – Zadanie 2

# Nowe elementy zadania 2:

# docker run -e NAME=Alice -p 8000:8000 my-app
# docker run -e NAME=Bob -p 8000:8000 my-app

# ------------------------------------------------------------

# TESTING – Zadanie 3 – Mapowanie portów

# Nowe elementy zadania 3:

# docker run -p 3000:8000 my-app

# ------------------------------------------------------------

# TESTING – Zadanie 4 – Wolumin dla danych

# Nowe elementy zadania 4:

# docker volume create app-logs
# docker run -p 3000:8000 -v app-logs:/app/logs --name app-with-volume my-app

# docker volume inspect app-logs

# docker stop app-with-volume
# docker rm app-with-volume

# docker run -p 3000:8000 -v app-logs:/app/logs --name app-with-volume my-app
