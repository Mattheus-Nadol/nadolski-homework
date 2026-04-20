import asyncio
import random

async def losowe_zadanie(nazwa):
    # Śpi losowy czas 1-10s i zwraca informację
    czas = random.randint(1, 10)
    await asyncio.sleep(czas)
    return f"{nazwa} zakończyło się po {czas} sekundach"

async def main():
    # Tworzymy 5 zadań jako Taski
    zadania = [asyncio.create_task(losowe_zadanie(f"Zadanie {i+1}")) for i in range(5)]
    
    # Czekamy na pierwsze zakończone zadanie
    done, pending = await asyncio.wait(zadania, return_when=asyncio.FIRST_COMPLETED)
    # asyncio.wait() czeka na taski z listy
    # return_when=asyncio.FIRST_COMPLETED oznacza, że zakończymy oczekiwanie
    # gdy przynajmniej jedno zadanie się zakończy
    # 'done' to zbiór (set) tasków, które się zakończyły
    # 'pending' to zbiór tasków, które wciąż trwają

    # Wypisujemy wynik jednego pierwszego zadania
    print("Pierwsze zakończone zadanie:", await done.pop())

asyncio.run(main())