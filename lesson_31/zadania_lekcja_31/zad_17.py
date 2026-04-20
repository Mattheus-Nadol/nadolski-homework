"""
Moduł symulujący pobieranie danych użytkownika, postów oraz komentarzy asynchronicznie.

Typy danych:
- int: identyfikator użytkownika lub posta
- List[Dict[str, Any]]: lista słowników reprezentujących posty lub komentarze

Źródła dokumentacji:
- asyncio: https://docs.python.org/3/library/asyncio.html
- typing: https://docs.python.org/3/library/typing.html
- time: https://docs.python.org/3/library/time.html
"""

import asyncio
import time
from typing import List, Dict, Any


async def pobierz_id_uzytkownika() -> int:
    """
    Symuluje pobranie ID użytkownika.
    """
    await asyncio.sleep(1)  # symulacja opóźnienia
    return 42


async def pobierz_posty(user_id: int) -> List[Dict[str, Any]]:
    """
    Symuluje pobranie listy postów dla danego użytkownika.

    :param user_id: ID użytkownika
    :return: lista postów (każdy post to słownik z kluczem 'post_id')
    """
    await asyncio.sleep(2)  # symulacja opóźnienia
    return [{"post_id": 1}, {"post_id": 2}, {"post_id": 3}, {"post_id": 4}]


async def pobierz_komentarze(post_id: int) -> List[Dict[str, Any]]:
    """
    Symuluje pobranie komentarzy dla danego postu.

    :param post_id: ID posta
    :return: lista komentarzy (każdy komentarz to słownik)
    """
    await asyncio.sleep(1)  # symulacja opóźnienia
    return [{"comment_id": 1, "post_id": post_id, "text": "Komentarz 1"},
            {"comment_id": 2, "post_id": post_id, "text": "Komentarz 2"}]


async def main() -> None:
    start_time = time.perf_counter()

    user_id = await pobierz_id_uzytkownika()
    posty = await pobierz_posty(user_id)

    # pobieranie komentarzy dla wszystkich postów współbieżnie
    komentarze_wszystkich_postow = await asyncio.gather(
        *(pobierz_komentarze(post["post_id"]) for post in posty)
    )
    # spłaszczenie listy komentarzy za pomocą list comprehension
    komentarze_wszystkich_postow = [komentarz for sublist in komentarze_wszystkich_postow for komentarz in sublist]

    end_time = time.perf_counter()

    print(f"User ID: {user_id}")
    print(f"Posty: {posty}")
    print(f"Komentarze: {komentarze_wszystkich_postow}")
    print(f"Czas wykonania: {end_time - start_time:.2f} sekundy")


if __name__ == "__main__":
    asyncio.run(main())
