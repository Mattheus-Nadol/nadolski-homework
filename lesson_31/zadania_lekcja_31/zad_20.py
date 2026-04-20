"""
Plik demonstruje użycie asynchronicznej funkcji (korutyny) z wykorzystaniem asyncio oraz random.
Korutyna random_sleep śpi losowy czas od 1 do 5 sekund, a następnie jest uruchamiana z limitem czasu 3 sekundy.

Dokumentacja:
- asyncio: https://docs.python.org/3/library/asyncio.html
- random: https://docs.python.org/3/library/random.html
"""
import asyncio
import random


async def random_sleep() -> None:
    """Korutyna śpi losowy czas od 1 do 5 sekund."""
    sleep_time = random.randint(1, 5)
    print(f"Sleeping for {sleep_time} seconds.")
    await asyncio.sleep(sleep_time)
    print("Finished sleeping.")


async def main() -> None:
    """Uruchomienie korutyny random_sleep z ograniczeniem czasowym 3 sekund."""
    try:
        await asyncio.wait_for(random_sleep(), timeout=3)
    except asyncio.TimeoutError:
        print("Timeout: coroutine took longer than 3 seconds.")


if __name__ == "__main__":
    asyncio.run(main())
