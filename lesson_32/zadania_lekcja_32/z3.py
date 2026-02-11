"""
Prosty serwer aiohttp z dynamicznym powitaniem.

Serwer obsługuje:
- '/' – statyczną stronę powitalną
- '/witaj/{imie}' – dynamiczne powitanie na podstawie imienia z URL
"""

from aiohttp import web


async def handle_root(request):
    return web.Response(
        text="<h1>Witaj na mojej stronie!</h1>",
        content_type="text/html"
    )


async def handle_witaj(request):
    imie = request.match_info["imie"]
    return web.Response(text=f"Witaj, {imie}!")


def create_app():
    app = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/witaj/{imie}", handle_witaj)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)