import asyncio
import random
import time

async def dlugie_obliczenia():
    # Losowy czas od 2 do 5 sekund
    await asyncio.sleep(random.uniform(2, 5))
    # Zwraca losową liczbę całkowitą od 1 do 100
    return random.randint(1, 100)

async def main():
    start_time = time.time()
    # Tworzymy listę 10 korutyn
    zadania = [dlugie_obliczenia() for _ in range(10)]
    
    # Uruchamiamy wszystkie współbieżnie i czekamy na wyniki
    wyniki = await asyncio.gather(*zadania)
    stop_time = time.time()
    # Sumujemy wyniki i wypisujemy
    suma = sum(wyniki)
    print("Wyniki poszczególnych zadań:", wyniki)
    print("Suma wszystkich wyników:", suma)
    print(f"Całkowity czas wykonania: {stop_time-start_time:.2f} sek.")

# Start programu
asyncio.run(main())