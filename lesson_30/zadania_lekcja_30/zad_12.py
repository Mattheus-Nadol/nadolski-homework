"""
Przykład pokazujący wpływ Global Interpreter Lock (GIL) na wykonywanie równoległe wątków w Pythonie.
Używamy modułów `threading` i `time` do pomiaru czasu wykonania operacji CPU-bound.

Dokumentacja:
- threading: https://docs.python.org/3/library/threading.html
- time: https://docs.python.org/3/library/time.html
"""

import threading
import time
from typing import Callable


def count_down(n: int) -> None:
    """
    Odlicza od n do 0, wykonując pętlę CPU-bound.

    Args:
        n (int): liczba, od której zaczynamy odliczanie
    """
    while n > 0:
        n -= 1


def measure_time(func: Callable, *args, **kwargs) -> float:
    """
    Mierzy czas wykonania funkcji.

    Args:
        func (Callable): funkcja do wykonania
        *args: argumenty pozycyjne funkcji
        **kwargs: argumenty nazwane funkcji

    Returns:
        float: czas wykonania w sekundach
    """
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    return end - start


def run_single_thread() -> None:
    """
    Wykonuje dwukrotnie funkcję count_down w jednym wątku i mierzy czas.
    """
    print("Wykonywanie count_down dwukrotnie w jednym wątku...")
    elapsed = measure_time(lambda: (count_down(10**7), count_down(10**7)))
    print(f"Czas wykonania (single thread): {elapsed:.4f} sekund")
    # Wykonanie w jednym wątku oznacza, że operacje są wykonywane sekwencyjnie.
    # Ponieważ jest to zadanie CPU-bound, cały czas procesora jest poświęcony na wykonanie jednej funkcji po drugiej.


def run_multi_thread() -> None:
    """
    Wykonuje funkcję count_down dwukrotnie w dwóch osobnych wątkach i mierzy czas.
    """
    print("Wykonywanie count_down dwukrotnie w dwóch wątkach...")

    thread1 = threading.Thread(target=count_down, args=(10**7,))
    thread2 = threading.Thread(target=count_down, args=(10**7,))

    start = time.perf_counter()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    end = time.perf_counter()

    print(f"Czas wykonania (multi thread): {end - start:.4f} sekund")
    # Pomimo uruchomienia dwóch wątków, czas wykonania nie jest znacząco krótszy niż w przypadku pojedynczego wątku.
    # Wynika to z Global Interpreter Lock (GIL), który pozwala na wykonanie kodu Pythona tylko w jednym wątku na raz,
    # co ogranicza równoległość w zadaniach CPU-bound.


if __name__ == "__main__":
    run_single_thread()
    run_multi_thread()
