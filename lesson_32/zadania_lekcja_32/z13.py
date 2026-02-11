"""
Prosty skrypt klienta aiohttp, który pobiera dane z 3 publicznych API równolegle przy użyciu asyncio.gather.

Skrypt pobiera:
1. Cenę Bitcoina z Binance (BTC/USDT),
2. Cenę Bitcoina z CoinGecko,
3. Losowy obraz psa z Dog CEO.

Wszystkie zapytania są wykonywane równolegle dla efektywności.
"""

import asyncio
import aiohttp

async def fetch(session, url):
    # Korutyna pobierająca JSON z podanego URL
    async with session.get(url) as response:
        return await response.json()

async def main():
    # Lista URL-i do pobrania
    urls = [
        'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT',
        'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd',
        'https://dog.ceo/api/breeds/image/random'
    ]

    async with aiohttp.ClientSession() as session:
        # Pobieramy wszystkie dane równolegle
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    # Wypisujemy pobrane dane JSON
    for i, data in enumerate(results, 1):
        print(f"Dane z API {i}: {data}")

# Uruchomienie głównej korutyny
asyncio.run(main())
