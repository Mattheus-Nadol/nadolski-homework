"""
Moduł do sprawdzania, które liczby z listy są liczbami pierwszymi,
z wykorzystaniem multiprocessing.Pool.

Generuje listę 100 losowych liczb z zakresu 1-1000, a następnie równolegle
sprawdza, które z nich są pierwsze. Na końcu wyświetla liczbę liczb pierwszych.
"""

import random
from multiprocessing import Pool
from typing import List

def is_prime(n: int) -> bool:
    """
    Sprawdza, czy liczba n jest liczbą pierwszą.

    :param n: liczba całkowita do sprawdzenia
    :return: True jeśli n jest liczbą pierwszą, False w przeciwnym wypadku
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def main() -> None:
    """
    Główna funkcja programu. Generuje listę 100 losowych liczb,
    sprawdza, które są pierwsze, i drukuje wynik.
    """
    # Generowanie listy 100 losowych liczb od 1 do 1000
    numbers: List[int] = [random.randint(1, 1000) for _ in range(100)]

    # Tworzenie puli procesów do równoległego sprawdzania liczb pierwszych
    with Pool() as pool:
        results: List[bool] = pool.map(is_prime, numbers)

    # Liczenie ile liczb jest pierwszych
    prime_count = sum(results)

    print(f"Liczba liczb pierwszych w liście: {prime_count}")

if __name__ == "__main__":
    main()
