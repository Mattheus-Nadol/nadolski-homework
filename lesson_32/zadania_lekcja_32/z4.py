from aiohttp import web
import json # Do obsługi błędów JSON
import datetime
import time

async def handle_data_demo(request: web.Request):
    """
    Handler demonstrujący odczyt różnych typów danych.
    Obsługuje POST na /api/demo/{id_uzytkownika}?kategoria=test
    """

    # Zwracamy odpowiedź jako JSON używając web.json_response
    response_data = {
        "status": "OK",
        "server_time" : str(datetime.datetime.now()),
        "another_time": time.time()

    }

    return web.json_response(response_data, status=200)


app = web.Application()
# Ścieżka dynamiczna: {id} zostanie przechwycone
app.router.add_get("/api/status/", handle_data_demo)

if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=8080)
    # dodano host, gdyż domyślnie był 0.0.0.0:8080