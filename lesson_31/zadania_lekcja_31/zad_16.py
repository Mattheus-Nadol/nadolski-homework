"""
zad_16.py - Asynchroniczny Rate Limiter w Pythonie

Ten moduł implementuje klasę RateLimiter, która pozwala na wykonanie
maksymalnie n wywołań metody acquire() na sekundę. Jeśli limit jest przekroczony,
wywołanie acquire() asynchronicznie czeka odpowiedni czas, aby nie przekroczyć
ustalonego limitu.

Testowa funkcja uruchamia 20 zadań współbieżnie, pokazując działanie limitera
przy limicie 5 wywołań/sekundę.

Źródła / dokumentacja:
- asyncio: https://docs.python.org/3/library/asyncio.html
- asyncio.create_task / asyncio.gather: https://docs.python.org/3/library/asyncio-task.html
- asyncio.Lock: https://docs.python.org/3/library/asyncio-sync.html#asyncio.Lock
- time.monotonic: https://docs.python.org/3/library/time.html#time.monotonic
"""

import asyncio
import time
from typing import List


class RateLimiter:
    """
    Asynchroniczny limiter wywołań, pozwalający na maksymalnie
    max_calls_per_sec wywołań metody acquire() na sekundę.
    """
    def __init__(self, max_calls_per_sec: int) -> None:
        self.max_calls: int = max_calls_per_sec
        self.call_times: List[float] = []
        self.lock: asyncio.Lock = asyncio.Lock()

    async def acquire(self) -> None:
        """
        Asynchronicznie czeka, jeśli limit wywołań na sekundę został przekroczony,
        w przeciwnym razie pozwala na natychmiastowe wykonanie.
        """
        async with self.lock:
            now: float = time.monotonic()
            # Usuwamy stare wpisy starsze niż 1 sekunda
            self.call_times = [t for t in self.call_times if now - t < 1]

            if len(self.call_times) >= self.max_calls:
                # Ile trzeba czekać, aby być w limicie
                sleep_time: float = 1 - (now - self.call_times[0])
                await asyncio.sleep(sleep_time)
                now = time.monotonic()
                self.call_times = [t for t in self.call_times if now - t < 1]

            self.call_times.append(time.monotonic())


async def task(rate_limiter: RateLimiter, nr: int) -> None:
    """
    Zadanie testowe, które korzysta z rate limiter i wypisuje informację o wykonaniu.
    """
    await rate_limiter.acquire()
    print(f"Zadanie {nr} wykonane o {time.strftime('%X')}")


async def main() -> None:
    """
    Uruchamia 20 zadań współbieżnie z limitem 5 wywołań na sekundę.
    """
    rate_limiter = RateLimiter(max_calls_per_sec=5)  # 5 wywołań na sekundę
    zadania = [asyncio.create_task(task(rate_limiter, i + 1)) for i in range(20)]

    await asyncio.gather(*zadania)


asyncio.run(main())