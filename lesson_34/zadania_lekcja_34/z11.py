"""
WebSocket Ping-Pong Server (aiohttp)
------------------------------------
Ten moduł implementuje serwer WebSocket, który obsługuje mechanizm ping-pong do utrzymania połączeń z klientami.

Funkcjonalności:
- Serwer co 30 sekund wysyła wszystkim klientom wiadomość "ping".
- Klient powinien odpowiedzieć "pong" w ciągu 60 sekund.
- Jeśli klient nie odpowie "pong" przez 60 sekund, serwer rozłącza klienta.
- Każde inne wiadomości tekstowe są odsyłane do klienta z prefiksem "Server: ".
"""

import asyncio
import time
from aiohttp import web

# Globalna struktura przechowująca połączenia i czas ostatniego 'pong'
# Klucz: websocket, Wartość: timestamp ostatniego 'pong'
connections = {}

PING_INTERVAL = 30      # co ile sekund wysyłać 'ping'
PONG_TIMEOUT = 60       # po ilu sekundach braku 'pong' rozłączyć klienta

async def ping_pong_task():
    """
    Zadanie okresowo wysyłające 'ping' do wszystkich klientów
    i rozłączające tych, którzy nie odpowiedzieli 'pong' w czasie.
    """
    while True:
        await asyncio.sleep(PING_INTERVAL)
        now = time.time()
        to_disconnect = []
        for ws, last_pong in list(connections.items()):
            # Wysyłamy 'ping' do klienta
            try:
                await ws.send_str("ping")
            except Exception:
                # Jeśli nie można wysłać, oznacz do rozłączenia
                to_disconnect.append(ws)
                continue
            # Sprawdzamy czy klient odpowiedział 'pong' w ciągu timeouta
            if now - last_pong > PONG_TIMEOUT:
                to_disconnect.append(ws)
        # Rozłączamy klientów, którzy nie odpowiedzieli 'pong'
        for ws in to_disconnect:
            try:
                await ws.close(message=b"No pong received")
            except Exception:
                pass
            connections.pop(ws, None)

async def websocket_handler(request):
    """
    Handler obsługujący połączenia WebSocket.
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    # Dodajemy klienta do connections z czasem bieżącym
    connections[ws] = time.time()
    try:
        async for msg in ws:
            # Obsługa tylko wiadomości tekstowych
            if msg.type == web.WSMsgType.TEXT:
                if msg.data == "pong":
                    # Aktualizujemy timestamp ostatniego 'pong'
                    connections[ws] = time.time()
                else:
                    # Echo z prefixem "Server: "
                    await ws.send_str(f"Server: {msg.data}")
            elif msg.type == web.WSMsgType.ERROR:
                # Błąd połączenia
                break
    finally:
        # Usuwamy klienta z connections przy rozłączeniu
        connections.pop(ws, None)
    return ws

app = web.Application()
# Rejestrujemy endpoint WebSocket
app.router.add_get('/ws', websocket_handler)

# Uruchamiamy zadanie ping-pong przy starcie serwera
async def on_startup(app):
    app['ping_pong_task'] = asyncio.create_task(ping_pong_task())

# Zatrzymujemy zadanie przy zamknięciu serwera
async def on_cleanup(app):
    app['ping_pong_task'].cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await app['ping_pong_task']

import contextlib
app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

if __name__ == "__main__":
    # Uruchamiamy serwer na 127.0.0.1:8765
    web.run_app(app, host="127.0.0.1", port=8765)

"""
Sekcja testowania:

1. Uruchom serwer:
   python z11.py

2. Otwórz przeglądarkę → DevTools → Console

3. Połącz klienta:

   let ws = new WebSocket("ws://127.0.0.1:8765/ws");

   ws.onopen = () => console.log("Połączono");

   ws.onmessage = (event) => {
       console.log("Serwer:", event.data);

       // Automatyczna odpowiedź na ping
       if(event.data === "ping"){
           ws.send("pong");
       }
   };

Test ręczny:
- Gdy pojawi się "ping" w konsoli,
  wpisz ręcznie:

  ws.send("pong");

Obserwacja:
- Brak pong przez 60 sekund spowoduje disconnect.
"""