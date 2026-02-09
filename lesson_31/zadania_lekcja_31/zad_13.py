"""https://docs.python.org/3/library/asyncio-stream.html"""
import asyncio

# Funkcja obsługująca połączenie z klientem
async def handle_client(reader, writer):
    # Odczytujemy dane od klienta (do 100 bajtów)
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    
    print(f"Otrzymano od {addr}: {message}")
    
    # Odsyłamy tę samą wiadomość
    writer.write(data)
    await writer.drain()  # czekamy, aż dane zostaną wysłane
    
    # Zamykamy połączenie
    writer.close()
    await writer.wait_closed()
    print(f"Połączenie z {addr} zamknięte")

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    
    addr = server.sockets[0].getsockname()
    print(f"Serwer działa na {addr}")
    
    async with server:
        await server.serve_forever()

# Uruchamiamy serwer
asyncio.run(main())

# Serwer nasłuchuje w nieskończoność
# Test echo
# W terminalu  nc 127.0.0.1 8888
# 'Hello, it's me'