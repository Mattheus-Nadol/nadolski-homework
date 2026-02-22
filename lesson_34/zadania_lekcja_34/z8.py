"""
Serwer WebSocket oparty na aiohttp, który mierzy czas trwania połączenia każdego klienta.
Po zakończeniu połączenia czas trwania jest wypisywany w konsoli serwera.
"""

# Importujemy potrzebne moduły
import asyncio
import time
from aiohttp import web

# Handler obsługujący połączenie WebSocket
async def websocket_handler(request):
    # Tworzymy obiekt WebSocketResponse
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Zapamiętujemy czas rozpoczęcia połączenia
    start_time = time.time()
    print("Nowe połączenie WebSocket")

    try:
        # Odbieramy wiadomości od klienta w pętli
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                # Odpowiadamy klientowi (echo z prefiksem)
                await ws.send_str(f"Server: {msg.data}")
            elif msg.type == web.WSMsgType.ERROR:
                print(f"Błąd podczas komunikacji WebSocket: {ws.exception()}")
    finally:
        # Obliczamy czas trwania połączenia
        duration = time.time() - start_time
        print(f"Połączenie zakończone. Czas trwania: {duration:.2f} sekundy")

    return ws

# Tworzymy aplikację aiohttp
app = web.Application()
# Dodajemy endpoint WebSocket pod ścieżką /ws
app.router.add_get('/ws', websocket_handler)

# Uruchamiamy serwer na localhost:8765
if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8765)

"""
Instrukcja testowania:
1. Uruchom ten serwer.
2. Otwórz przeglądarkę i przejdź do dowolnej strony.
3. Otwórz konsolę JS (F12 -> Console) i wpisz:

   let ws = new WebSocket('ws://localhost:8765/ws');
   ws.onmessage = e => console.log('Odpowiedź z serwera:', e.data);
   ws.onopen = () => ws.send('Hello!');
   // Po kilku wiadomościach zamknij połączenie:
   ws.close();

4. Po zamknięciu połączenia sprawdź konsolę serwera – powinien pojawić się czas trwania połączenia.
"""