"""
Moduł WebSocket Chat Server (aiohttp)

Opis techniczny:
- Serwer chatowy oparty o WebSocket.
- Endpoint komunikacyjny: /chat
- Port serwera: 8080
- Obsługa wielu jednoczesnych klientów.
- Mechanizm broadcast wiadomości.
- Pierwsza wiadomość od klienta traktowana jest jako identyfikator użytkownika (nick).
- Kolejne wiadomości są rozsyłane do wszystkich pozostałych klientów.
- Stan połączeń przechowywany jest w pamięci procesu.
- Obsługa rozłączenia klienta z powiadomieniem broadcast.
"""
from aiohttp import web
import asyncio
from typing import Set

active_connections: Set[web.WebSocketResponse] = set()

async def broadcast_message(message: str, sender: web.WebSocketResponse = None):
    for connection in active_connections:
        if connection != sender and not connection.closed:
            try:
                await connection.send_str(message)
            except Exception as e:
                print(f"❌ Błąd wysyłania do klienta: {e}")

async def chat_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    active_connections.add(ws)
    print(f"✅ Nowy klient! Łącznie połączeń: {len(active_connections)}")

    username = None
    
    await broadcast_message(
        f"🟢 Nowy użytkownik dołączył! Aktywnych: {len(active_connections)}",
        sender=ws
    )
    
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                if username is None:
                    username = msg.data.strip()
                    print(f"👤 Ustawiono nazwę użytkownika: {username}")
                    await broadcast_message(
                        f"🟢 Użytkownik '{username}' dołączył! Aktywnych: {len(active_connections)}",
                        sender=ws
                    )
                else:
                    user_message = msg.data
                    print(f"💬 Wiadomość od {username}: {user_message}")
                    await broadcast_message(f"💬 {username}: {user_message}")
            elif msg.type == web.WSMsgType.ERROR:
                print(f"❌ Błąd WebSocket: {ws.exception()}")
    
    finally:
        active_connections.discard(ws)
        print(f"❌ Klient rozłączony. Zostało: {len(active_connections)}")
        if username:
            await broadcast_message(
                f"🔴 Użytkownik '{username}' opuścił chat. Aktywnych: {len(active_connections)}"
            )
        else:
            await broadcast_message(
                f"🔴 Użytkownik opuścił chat. Aktywnych: {len(active_connections)}"
            )
    return ws

app = web.Application()
app.router.add_get('/chat', chat_handler)

if __name__ == '__main__':
    print("🚀 Chat server działa na ws://localhost:8080/chat")
    web.run_app(app, host='localhost', port=8080)


# ==========================
# TESTOWANIE
# ==========================

# 1. Uruchom serwer, wykonując ten plik (python z9.py).
# 2. Otwórz w przeglądarce lub w narzędziu do WebSocket (np. Postman, Insomnia) adres ws://localhost:8080/chat.
# 3. Połącz się jako pierwszy klient i wyślij swoją nazwę użytkownika jako pierwszą wiadomość.
# 4. Otwórz kolejne okno przeglądarki lub klienta WebSocket i połącz się jako drugi klient, również przesyłając nazwę użytkownika jako pierwszą wiadomość.
# 5. Po ustawieniu nazwy użytkownika możesz wysyłać wiadomości, które będą rozsyłane do wszystkich klientów.
# 6. Powtórz wysyłanie wiadomości z różnych klientów, sprawdzając, czy komunikaty się poprawnie rozsyłają.
# 7. Zamknij jedno z połączeń i sprawdź, czy pozostali użytkownicy otrzymują powiadomienie o rozłączeniu.
# 8. Przetestuj przypadek błędu (np. przerwij połączenie nagle) i obserwuj logi serwera.
# 9. Sprawdź, czy połączenia się poprawnie zamykają i czy nowe połączenia są dodawane do zbioru aktywnych.
# 10. Po zakończeniu testów zatrzymaj serwer (Ctrl+C).

# ==========================
# PRZYKŁADOWE KOMENDY JAVASCRIPT DO KONSOLI PRZEGLĄDARKI
# ==========================

# // 1. Połączenie i konfiguracja ws (wszystkie komendy do wklejenia na raz)
# const ws = new WebSocket('ws://localhost:8080/chat');
# ws.onmessage = (event) => {
#     console.log('Otrzymano:', event.data);
# };
# ws.onopen = () => {
#     console.log('Połączenie WebSocket otwarte');
# };
# ws.onclose = () => {
#     console.log('Połączenie WebSocket zamknięte');
# };

# // 2. Wysyłanie nazwy użytkownika jako pierwszej wiadomości (komendy do wywoływania osobno)
# ws.send('TwojaNazwaUżytkownika');

# // 3. Wysyłanie wiadomości po ustawieniu nazwy użytkownika
# ws.send('Cześć wszystkim!');

# // 4. Zamykanie połączenia (komendy do wywoływania osobno)
# ws.close();
