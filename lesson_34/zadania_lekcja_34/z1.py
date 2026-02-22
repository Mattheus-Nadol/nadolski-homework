import asyncio
from aiohttp import web


async def echo(request: web.Request) -> web.WebSocketResponse:
    """
    Prosty serwer WebSocket (echo server).

    Po nawiązaniu połączenia:
    - odbiera wiadomość tekstową od klienta,
    - odsyła ją z powrotem z prefiksem "Server: ".

    Parametry:
        request (web.Request): Obiekt żądania HTTP inicjujący połączenie WebSocket.

    Zwraca:
        web.WebSocketResponse: Obiekt WebSocket obsługujący komunikację.
    """

    # Tworzymy obiekt WebSocketResponse (reprezentuje połączenie z klientem)
    ws = web.WebSocketResponse()

    # Wykonujemy handshake HTTP -> WebSocket
    await ws.prepare(request)

    print("Nowe połączenie WebSocket")

    # Pętla odbierająca wiadomości od klienta
    async for msg in ws:

        # Obsługa wiadomości tekstowych
        if msg.type == web.WSMsgType.TEXT:
            print(f"Odebrano: {msg.data}")

            # Odesłanie wiadomości z prefiksem "Server: "
            await ws.send_str(f"Server: {msg.data}")

        # Obsługa błędów połączenia
        elif msg.type == web.WSMsgType.ERROR:
            print(f"Błąd połączenia: {ws.exception()}")

    print("Połączenie zamknięte")
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

const ws = new WebSocket('ws://localhost:8765/ws');

ws.onmessage = (event) => console.log('Otrzymano:', event.data);
ws.onopen = () => console.log('Połączenie otwarte');
ws.onclose = () => console.log('Połączenie zamknięte');
ws.onerror = (e) => console.error('Błąd:', e);

// Wysyłanie wiadomości:
// ws.send("Cześć");
"""