import asyncio

async def oblicz_potege(liczba, potega):
    await asyncio.sleep(2)
    return liczba ** potega

async def main():
    wynik = await oblicz_potege(12, 2)
    print(f"Wynik: {wynik}")

asyncio.run(main())