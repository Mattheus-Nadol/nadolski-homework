"""
Prosty serwer aiohttp z odczytem parametrów query.

Endpoint '/api/search' odczytuje parametr 'q' z zapytania GET i zwraca JSON.
"""

from aiohttp import web

async def handle_search(request):
    q = request.query.get("q")
    if q:
        return web.json_response({"szukana_fraza": q})
    return web.json_response({"błąd": "Brak parametru q"})

def create_app():
    app = web.Application()
    app.router.add_get("/api/search", handle_search)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)
