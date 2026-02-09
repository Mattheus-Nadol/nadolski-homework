import asyncio

async def licznik(n):
    for i in range(1, n+1):
        await asyncio.sleep(1)
        print(i)
    return "Zakończono licznik"

async def main():
    wynik = await licznik(8)
    print(wynik)

# Uruchomienie głównej korutyny 'main'
asyncio.run(main())