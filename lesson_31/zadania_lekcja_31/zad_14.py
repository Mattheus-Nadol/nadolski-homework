import asyncio
import random

async def producent(kolejka, liczba_konsumentow):
    # Producent generuje liczby od 1 do 20 i umieszcza je w kolejce
    for i in range(1, 21):
        await asyncio.sleep(0.5)  # symulacja opóźnienia produkcji
        await kolejka.put(i)
        print(f"Producent dodał: {i}")
    # Po dodaniu wszystkich liczb, producent dodaje tyle None, ile jest konsumentów,
    # aby każdy konsument mógł odebrać sygnał zakończenia pracy
    for _ in range(liczba_konsumentow):
        await kolejka.put(None)

async def konsument(kolejka, numer):
    while True:
        liczba = await kolejka.get()  # pobieramy element z kolejki
        if liczba is None:
            # Jeśli otrzymamy None, oznacza to koniec pracy konsumenta
            kolejka.task_done()
            break
        # Przetwarzamy pobraną liczbę (tu: tylko ją wypisujemy)
        print(f"Konsument {numer} przetworzył liczbę: {liczba}")
        kolejka.task_done()  # sygnalizujemy, że zadanie zostało wykonane
        await asyncio.sleep(random.uniform(0.1, 1))  # symulujemy czas przetwarzania

async def main():
    kolejka = asyncio.Queue()  # tworzymy asynchroniczną kolejkę
    liczba_konsumentow = 2     # definiujemy liczbę konsumentów

    # Tworzymy zadanie producenta
    prod_task = asyncio.create_task(producent(kolejka, liczba_konsumentow))
    # Tworzymy zadania konsumentów
    konsumenci = [asyncio.create_task(konsument(kolejka, i+1)) for i in range(liczba_konsumentow)]

    await prod_task  # czekamy na zakończenie producenta
    await kolejka.join()  # czekamy aż wszystkie elementy z kolejki zostaną przetworzone

    # Czekamy aż wszyscy konsumenci zakończą pracę
    await asyncio.gather(*konsumenci)

asyncio.run(main())