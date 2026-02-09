"""
Docstring for Zadanie 9:
https://docs.aiohttp.org/en/stable/
"""
import aiohttp
import asyncio
import ssl

async def fetch(session, url):
    # Tworzymy kontekst SSL, który nie weryfikuje certyfikatów
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async with session.get(url, ssl=ssl_context) as response:
            return f"{url} - Status: {response.status}"
    except Exception as e:
        return f"{url} - Błąd: {e}"

async def main():
    urls = [
        "https://google.com",
        "https://python.org",
        "https://nonexistent.url",
        "https://github.com",
        "https://stackoverflow.com"
    ]

    # Jedna sesja dla wszystkich zapytań
    async with aiohttp.ClientSession() as session:
        zadania = [fetch(session, url) for url in urls]
        wyniki = await asyncio.gather(*zadania)

        for wynik in wyniki:
            print(wynik)

asyncio.run(main())