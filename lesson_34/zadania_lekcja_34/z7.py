"""
Prosty serwer WebSocket z mechanizmem broadcast (aiohttp).

Techniczne założenia:
- Serwer oparty o aiohttp.
- Endpoint WebSocket dostępny pod ścieżką /ws.
- Globalny zbiór przechowujący aktywne połączenia.
- Każda otrzymana wiadomość tekstowa jest rozsyłana do wszystkich aktualnie podłączonych klientów.
- Obsługa wielu jednoczesnych połączeń w sposób asynchroniczny.
"""

import asyncio
from aiohttp import web

# Globalny zbiór przechowujący aktywne połączenia WebSocket
connected_clients = set()

async def websocket_handler(request):
    """
    Obsługuje połączenia WebSocket.
    Dodaje klienta do zbioru, odbiera wiadomości i rozsyła je do wszystkich klientów.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Dodaj klienta do zbioru aktywnych połączeń
    connected_clients.add(ws)
    try:
        # Odbieraj wiadomości od klienta
        async for msg in ws:
            # Sprawdź, czy wiadomość jest tekstowa
            if msg.type == web.WSMsgType.TEXT:
                # Broadcast: wyślij wiadomość do wszystkich klientów
                for client in connected_clients:
                    # Sprawdź, czy połączenie jest nadal otwarte
                    if not client.closed:
                        await client.send_str(msg.data)
            elif msg.type == web.WSMsgType.ERROR:
                print(f"Błąd połączenia: {ws.exception()}")
    finally:
        # Usuń klienta ze zbioru po zamknięciu połączenia
        connected_clients.discard(ws)

    return ws

# Konfiguracja aplikacji aiohttp i dodanie endpointu WebSocket
app = web.Application()
app.router.add_get("/ws", websocket_handler)

if __name__ == "__main__":
    # Uruchom serwer na localhost:8765
    web.run_app(app, host="127.0.0.1", port=8765)

"""
Instrukcja testowania w przeglądarce:

1. Uruchom ten serwer (python z7.py).
2. Otwórz kilka kart w przeglądarce i w każdej z nich wpisz w konsoli JS:

   let ws = new WebSocket("ws://127.0.0.1:8765/ws");
   ws.onmessage = e => console.log("Odebrano:", e.data);

3. Aby wysłać wiadomość do wszystkich:

   ws.send("Cześć z tej karty!");

4. Każda wiadomość wysłana z jednej karty pojawi się we wszystkich otwartych kartach (broadcast).
5. Możesz otworzyć dowolną liczbę kart/klientów.
"""