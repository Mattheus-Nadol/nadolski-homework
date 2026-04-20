"""
Prosty serwer aiohttp, który obsługuje endpoint POST /api/v1/chat.
Oczekuje JSON z polem "prompt", symuluje przetwarzanie i zwraca odpowiedź.
"""

import asyncio
import time
from aiohttp import web

async def chat_handler(request):
    # Odczytujemy JSON z żądania
    data = await request.json()
    prompt = data.get("prompt", "")
    
    start_time = time.perf_counter()  # pomiar czasu został dodany w celach testowych
    # Symulujemy długie przetwarzanie AI
    await asyncio.sleep(3)
    elapsed_time = time.perf_counter() - start_time  # pomiar czasu został dodany w celach testowych
    
    # Tworzymy odpowiedź JSON
    response = {
        "response": f"Otrzymałem twój prompt: '{prompt}' i przetworzyłem go.",
        "elapsed_time": elapsed_time
    }
    return web.json_response(response)

def create_app():
    app = web.Application()
    # Rejestrujemy handler dla endpointu POST /api/v1/chat
    app.router.add_post("/api/v1/chat", chat_handler)
    return app

if __name__ == "__main__":
    app = create_app()
    # Uruchamiamy serwer aiohttp
    web.run_app(app, host="127.0.0.1", port=8080)
