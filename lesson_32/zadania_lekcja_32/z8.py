"""
Prosty serwer aiohttp.

Endpoint '/witaj/{imie}' zwraca powitanie dla podanego imienia.
Jeśli imię to 'admin', zwraca HTTP 403 Forbidden.
"""
from aiohttp import web

async def witaj(request):
    imie = request.match_info.get('imie', "Anonim")
    if imie == "admin":
        raise web.HTTPForbidden(text="Dostęp dla admina zabroniony")
    return web.Response(text=f"Witaj, {imie}!")

def create_app():
    app = web.Application()
    app.router.add_get('/witaj/{imie}', witaj)
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=8080)
