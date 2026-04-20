"""
Moduł zawierający asynchroniczny generator liczb pierwszych oraz funkcję główną do ich wyświetlania.
Źródła dokumentacji:
- asyncio: https://docs.python.org/3/library/asyncio.html
- Typy w Pythonie: https://docs.python.org/3/library/typing.html
"""

import asyncio
from typing import AsyncGenerator

async def async_prime_generator() -> AsyncGenerator[int, None]:
    """
    Asynchronous generator that yields prime numbers, one every 0.1 seconds.
    """
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    num = 2
    while True:
        if is_prime(num):
            await asyncio.sleep(0.1)
            yield num
        num += 1


async def main() -> None:
    """
    Main function that prints prime numbers up to 100 using async for.
    """
    async for prime in async_prime_generator():
        if prime > 100:
            break
        print(prime)


if __name__ == "__main__":
    asyncio.run(main())