"""
Prosty skrypt klienta aiohttp, który pobiera aktualną cenę Bitcoina w USD z API CoinDesk.

Więcej informacji o aiohttp można znaleźć pod adresem:
https://docs.aiohttp.org/en/stable/
"""

import asyncio
import aiohttp

async def main():
    # Oryginalny URL API CoinDesk ('https://api.coindesk.com/v1/bpi/currentprice.json') użyty w zadaniu zwracał 404 i już nie działa.
    # Zamiast tego używamy publicznego API Binance:
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            # Binance zwraca: {"symbol":"BTCUSDT","price":"xxxx.xx"}
            price_usd = data['price']
            print(f"Cena Bitcoina w USD: $ {float(price_usd):.2f}")

# Uruchom główną korutynę
# ten wzorzec jest przeznaczony dla samodzielnych klientów i nie używamy go w serwerach aiohttp
asyncio.run(main())
