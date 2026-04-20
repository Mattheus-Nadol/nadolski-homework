import asyncio

async def odliczanie(nazwa, start):
    for pozostało in range(start, 0, -1):
        print(f"{nazwa}: zostało {pozostało} sekund")
        await asyncio.sleep(1)
    print(f"{nazwa}: czas minął!")

async def main():
    # Tworzymy trzy korutyny z różnymi nazwami i czasami startowymi
    zadania = [
        odliczanie("Odliczanie A", 5),
        odliczanie("Odliczanie B", 3),
        odliczanie("Odliczanie C", 7)
    ]
    
    # Uruchamiamy wszystkie odliczania współbieżnie
    await asyncio.gather(*zadania)

# Startujemy program
asyncio.run(main())