import asyncio
from aiohttp import ClientSession


async def websocket_client():
    """
    Asynchroniczny klient WebSocket wykorzystujący bibliotekę aiohttp.

    Klient łączy się z serwerem pod adresem:
        ws://localhost:8765/ws

    Po nawiązaniu połączenia wysyła kolejno trzy wiadomości:
        1. "Cześć"
        2. "Jak się masz?"
        3. "Do widzenia"

    Po każdej wysłanej wiadomości klient oczekuje na odpowiedź serwera
    i wypisuje ją w konsoli.
    """

    url = "http://localhost:8765/ws"  # Adres endpointu WebSocket (w aiohttp używamy http:// przy ws_connect)

    # Tworzymy sesję HTTP (wymaganą przez aiohttp)
    async with ClientSession() as session:

        # Nawiązujemy połączenie WebSocket z serwerem
        async with session.ws_connect(url) as ws:
            print("Połączenie z serwerem zostało nawiązane.")

            # Lista wiadomości do wysłania
            messages = ["Cześć", "Jak się masz?", "Do widzenia"]

            for message in messages:
                # Wysyłamy wiadomość tekstową do serwera
                await ws.send_str(message)
                print(f"Wysłano: {message}")

                # Oczekujemy na odpowiedź od serwera
                msg = await ws.receive()

                # Sprawdzamy typ wiadomości
                if msg.type.name == "TEXT":
                    print(f"Otrzymano: {msg.data}")
                elif msg.type.name == "CLOSE":
                    print("Serwer zamknął połączenie.")
                    break
                elif msg.type.name == "ERROR":
                    print(f"Wystąpił błąd: {ws.exception()}")
                    break

            print("Zamykanie połączenia...")
            await ws.close()



if __name__ == "__main__":
    # Uruchamiamy klienta WebSocket w pętli zdarzeń asyncio
    asyncio.run(websocket_client())

"""
=============================
INSTRUKCJA TESTOWANIA
=============================

1️⃣  Uruchom najpierw serwer (np. z pliku z1.py):

    python z1.py

2️⃣  W nowym oknie terminala uruchom klienta:

    python z2.py

3️⃣  Oczekiwany rezultat:
    - Klient połączy się z serwerem.
    - Wyśle trzy wiadomości:
        "Cześć"
        "Jak się masz?"
        "Do widzenia"
    - Po każdej wiadomości otrzyma odpowiedź w formacie:
        Server: <wiadomość>

4️⃣  Po wysłaniu wszystkich wiadomości połączenie zostanie zamknięte.

Uwaga:
Serwer musi być uruchomiony przed startem klienta,
w przeciwnym razie pojawi się błąd połączenia.
"""
