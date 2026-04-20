"""
Program demonstruje asynchroniczne wykonywanie zadań w Pythonie.

Uruchamia trzy korutyny z różnymi opóźnieniami (1, 4 i 2 sekundy)
przy użyciu asyncio.gather(), mierzy całkowity czas wykonania
i pokazuje, że zadania wykonują się równolegle asynchronicznie,
a nie jedno po drugim.
"""
import asyncio
import time

async def zadanie(opoznienie):
    await asyncio.sleep(opoznienie)

async def main():
    start = time.time()

    await asyncio.gather(
        zadanie(1),
        zadanie(4),
        zadanie(2)
    )

    koniec = time.time()
    print(f"Czas wykonania: {koniec - start:.2f} sekundy")

if __name__ == "__main__":
    asyncio.run(main())