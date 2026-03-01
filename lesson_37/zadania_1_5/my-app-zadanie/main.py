# Aplikacja aiohttp – Zadanie 4 (Docker volume logging)

"""
Prosta aplikacja demonstracyjna aiohttp.

Funkcjonalność:
- Odczyt zmiennej środowiskowej NAME
- Zwracanie odpowiedzi HTTP
- Zapisywanie logów do pliku w Docker volume
"""

import os
from aiohttp import web

# ================================
# Katalog logów (Docker volume persistence)
# Katalog używany do przechowywania logów aplikacji wewnątrz wolumenu kontenera.
# Dane zapisane w tym katalogu przetrwają restart kontenera.
# ================================
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Tworzymy katalog logs przy starcie aplikacji
os.makedirs(LOG_DIR, exist_ok=True)

# Domyślna wartość nazwy użytkownika
DEFAULT_NAME = os.getenv("NAME", "Docker")

# ================================
# Handler HTTP
# ================================

async def handle(request):
    """
    Endpoint główny aplikacji.

    Każde wejście na "/" powoduje:
    - zapis logu do pliku
    - zwrócenie odpowiedzi HTTP
    """

    name = os.getenv("NAME", DEFAULT_NAME)

    # Upewniamy się, że katalog logów istnieje
    os.makedirs(LOG_DIR, exist_ok=True)

    log_line = f"Request received. NAME={name}\n"

    # Uwaga edukacyjna:
    # Blok try/except chroni operację zapisu pliku.
    # W systemach produkcyjnych zaleca się używanie frameworków logowania.
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)

        print("DEBUG:", log_line.strip(), flush=True)

    except Exception as e:
        print("Logging error:", str(e), flush=True)

    return web.Response(text=f"Hello, {name}!")

# ================================
# Konfiguracja routingu HTTP
# Mapowanie ścieżek URL na funkcje obsługi żądań
# ================================
app = web.Application()
app.router.add_get("/", handle)

# ================================
# Start serwera
# ================================

if __name__ == "__main__":
    print("Server starting on http://0.0.0.0:8000", flush=True)
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
