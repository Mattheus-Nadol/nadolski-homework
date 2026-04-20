############################################################
# (37) Projekt Dockerfile – Wersja Multi-stage
# Multi-stage build pozwala oddzielić środowisko budowania 
# od runtime i zmniejszyć rozmiar finalnego obrazu poprzez 
# usunięcie zbędnych narzędzi buildowych.
############################################################

###############################
# Etap 1 – Środowisko budowania (Builder)
#
# W tym etapie przygotowujemy środowisko potrzebne do:
# - instalacji zależności aplikacji
# - przygotowania kodu źródłowego
#
# Zaleta takiego podejścia:
# - finalny obraz Docker jest mniejszy
# - środowisko runtime nie zawiera narzędzi buildowych
###############################

FROM python:3.11-slim AS builder

# Ustawiamy katalog roboczy w kontenerze buildera
WORKDIR /app

############################################################
# Kopiowanie zależności – optymalizacja cache Dockera
#
# Najpierw kopiujemy requirements.txt ponieważ:
# - jeśli plik się nie zmieni, Docker użyje cache
# - przyspiesza to proces budowania obrazu
############################################################

COPY requirements.txt .

# Instalujemy biblioteki aplikacji
# Używamy flagi --no-cache-dir aby:
# - zmniejszyć rozmiar obrazu
# - nie przechowywać zbędnego cache Pythona
RUN pip install --no-cache-dir -r requirements.txt

############################################################
# Kopiowanie kodu aplikacji
#
# main.py zawiera logikę serwera aiohttp
# Kod aplikacji jest potrzebny do uruchomienia serwera
############################################################

COPY main.py .

############################################################
# Etap 2 – Środowisko runtime (minimalne)
#
# W tym etapie tworzymy finalny obraz uruchomieniowy,
# który zawiera tylko to, co jest potrzebne do działania aplikacji.
############################################################

FROM python:3.11-slim

# Ustawiamy katalog roboczy aplikacji
WORKDIR /app

############################################################
# Uprawnienia do katalogu logs – rozwiązanie problemu PermissionError
#
# Tworzymy katalog logs i ustawiamy pełne uprawnienia zapisu,
# aby aplikacja mogła zapisywać logi do Docker volume.
############################################################

RUN mkdir -p /app/logs && chmod -R 777 /app/logs

############################################################
# Instalacja zależności w środowisku runtime
#
# W multi-stage build same pliki projektu są kopiowane,
# ale biblioteki Python muszą być również dostępne
############################################################

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

############################################################
# Bezpieczeństwo – użytkownik bez uprawnień root
#
# Tworzymy użytkownika systemowego appuser,
# aby aplikacja nie działała z uprawnieniami administratora.
############################################################

RUN useradd -m appuser

############################################################
# Kopiowanie artefaktów z etapu builder
#
# Kopiujemy tylko przygotowane pliki aplikacji,
# co znacząco zmniejsza rozmiar finalnego obrazu.
############################################################

COPY --from=builder /app /app

############################################################
# Ustawiamy właściciela plików na użytkownika aplikacji
############################################################

RUN chown -R appuser:appuser /app

# Przełączamy się na użytkownika nie-root
USER appuser

############################################################
# Port aplikacji
#
# EXPOSE 8000 oznacza, że aplikacja nasłuchuje na porcie 8000
# Aby udostępnić port na hoście należy użyć:
# docker run -p 3000:8000 nazwa-obrazu
############################################################

EXPOSE 8000

############################################################
# Komenda startowa kontenera
#
# Uruchamia aplikację Python:
# python main.py
############################################################

CMD ["python", "main.py"]

############################################################
# NOTATKI – ZADANIA 2-5
#
# Zadanie 2 – zmienna środowiskowa NAME
# Można nadpisać przy uruchomieniu kontenera:
# docker run -e NAME=Alice my-app
#
# Zadanie 3 – mapowanie portów
# Host:3000 → Kontener:8000
#
# Zadanie 4 – trwałość danych (wolumen)
# Logi zapisywane są w katalogu /app/logs
#
# Zadanie 5 – Multi-stage build
# Oddzielenie etapu budowania od runtime zmniejsza rozmiar obrazu
############################################################