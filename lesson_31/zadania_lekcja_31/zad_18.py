"""Moduł demonstruje użycie asynchronicznej korutyny w Pythonie z obsługą anulowania zadania.
Korutyna 'pracuj' drukuje komunikat co sekundę i obsługuje wyjątek anulowania.
Dokumentacja asyncio: https://docs.python.org/3/library/asyncio.html
"""

import asyncio


async def pracuj() -> None:
    """Korutyna drukująca 'Pracuję...' co sekundę, obsługująca anulowanie."""
    try:
        while True:
            print("Pracuję...")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Anulowano, sprzątam...")
        raise


async def main() -> None:
    """Uruchamia korutynę pracuj, pozwala działać 5 sekund, a następnie ją anuluje."""
    task = asyncio.create_task(pracuj())
    await asyncio.sleep(5)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())
