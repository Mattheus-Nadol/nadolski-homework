"""
Prosty serwer aiohttp z API JSON.

Endpoint '/api/status' zwraca aktualny status serwera i czas.
"""

from aiohttp import web
from datetime import datetime


async def handle_status(request):
    now = datetime.now().isoformat()
    return web.json_response({
        "status": "OK",
        "server_time": now
    })


def create_app():
    app = web.Application()
    app.router.add_get("/api/status", handle_status)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)