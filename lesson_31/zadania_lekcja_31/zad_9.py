import asyncio
import aiohttp

async def check_status(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                return f"{url} - Status: {response.status}"
        except Exception as e:
            return f"{url} - Błąd: {e}"

async def main():
    urls = [
        "https://google.com",
        "https://python.org",
        "https://nonexistent.url",  # przykład błędu
        "https://github.com",
        "https://stackoverflow.com"
    ]

    # Tworzymy listę zadań dla wszystkich URLi
    zadania = [check_status(url) for url in urls]

    # Współbieżne wykonanie wszystkich zadań
    wyniki = await asyncio.gather(*zadania)

    # Wypisanie wyników
    for wynik in wyniki:
        print(wynik)

# Uruchamiamy pętlę asyncio
asyncio.run(main())