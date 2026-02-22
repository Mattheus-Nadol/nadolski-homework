import asyncio
from aiohttp import web

# Zmienna globalna przechowująca liczbę aktywnych połączeń
active_connections = 0


async def echo(request: web.Request) -> web.WebSocketResponse:
    """
    Serwer WebSocket z licznikiem aktywnych połączeń.

    Przy każdym nowym połączeniu:
    - zwiększa licznik aktywnych klientów,
    - wysyła do klienta informację o jego numerze,
    - działa jak klasyczny echo server (odsyła wiadomość z prefiksem "Server: "),
    - przy rozłączeniu zmniejsza licznik aktywnych klientów.
    """

    global active_connections  # Informujemy, że będziemy modyfikować zmienną globalną

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Zwiększamy licznik połączeń
    active_connections += 1
    client_number = active_connections

    print(f"Nowe połączenie. Aktywnych klientów: {active_connections}")

    # Wysyłamy do klienta informację o jego numerze
    await ws.send_str(f"Jesteś klientem numer {client_number}")

    try:
        async for msg in ws:

            if msg.type == web.WSMsgType.TEXT:
                print(f"Odebrano od klienta {client_number}: {msg.data}")
                await ws.send_str(f"Server: {msg.data}")

            elif msg.type == web.WSMsgType.ERROR:
                print(f"Błąd połączenia klienta {client_number}: {ws.exception()}")

    finally:
        # Zmniejszamy licznik przy rozłączeniu
        active_connections -= 1
        print(f"Klient {client_number} rozłączony. Aktywnych klientów: {active_connections}")

    return ws


def main() -> None:
    """
    Funkcja uruchamiająca aplikację aiohttp.

    Serwer będzie dostępny pod adresem:
        ws://localhost:8765/ws
    """

    # Tworzymy aplikację webową
    app = web.Application()

    # Rejestrujemy endpoint WebSocket pod ścieżką /ws
    app.router.add_get("/ws", echo)

    print("Serwer echo uruchomiony na ws://localhost:8765/ws")

    # Uruchamiamy serwer
    web.run_app(app, host="localhost", port=8765)


if __name__ == "__main__":
    main()


"""
TEST (konsola przeglądarki)

1️⃣  Otwórz kilka kart przeglądarki.
2️⃣  W każdej karcie otwórz DevTools → Console.
3️⃣  Wklej:

const ws = new WebSocket('ws://localhost:8765/ws');

ws.onmessage = (event) => console.log('Otrzymano:', event.data);
ws.onopen = () => console.log('Połączenie otwarte');
ws.onclose = () => console.log('Połączenie zamknięte');

Każda karta powinna otrzymać komunikat:
"Jesteś klientem numer X"

Następnie możesz testować echo:
ws.send("Test");
"""