"""
Prosty serwer aiohttp z obsługą POST i echo JSON.

Endpoint '/api/echo' odczytuje dane JSON z ciała zapytania i odsyła je z powrotem.
"""

import json
from aiohttp import web

async def handle_echo(request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"błąd": "Niepoprawny JSON"}, status=400)
    return web.json_response(data)

def create_app():
    app = web.Application()
    app.router.add_post("/api/echo", handle_echo)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)