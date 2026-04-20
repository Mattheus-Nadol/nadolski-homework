"""
Prosty serwer aiohttp.

Serwer nasłuchuje na localhost:8080 i na ścieżce '/'
zwraca stronę HTML z tekstem powitalnym.
"""

from aiohttp import web

async def handle_index(request):
    return web.Response(
        text="<h1>Witaj na mojej stronie!</h1>",
        content_type="text/html"
    )

def create_app():
    app = web.Application()
    app.router.add_get("/", handle_index)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)