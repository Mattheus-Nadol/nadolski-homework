import asyncio
import time

async def zadanie1():
    await asyncio.sleep(2)
    print("Zadanie 1 zakończone")
    return "1"

async def zadanie2():
    await asyncio.sleep(1)
    print("Zadanie 2 zakończone")
    return "2"

async def main():
    # Uruchamiamy korutyny jedna po drugiej (sekwencyjnie)
    start_time = time.time()
    await zadanie1()
    await zadanie2()
    stop_time = time.time()
    print(f"Czas wykonania: {stop_time-start_time:.2f}")

asyncio.run(main())