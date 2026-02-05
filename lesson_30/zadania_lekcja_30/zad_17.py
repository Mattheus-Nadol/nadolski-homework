"""
Moduł realizuje dwukierunkową komunikację między procesem nadrzędnym a potomnym
przy użyciu multiprocessing.Pipe. Proces nadrzędny wysyła listę liczb do procesu
potomnego, który oblicza sumę i średnią tych liczb i odsyła wyniki z powrotem.

Źródła i dokumentacja:
- multiprocessing: https://docs.python.org/3/library/multiprocessing.html
- multiprocessing.Pipe: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Pipe
"""

from multiprocessing import Process, Pipe
from typing import List


def child_process(conn) -> None:
    """
    Funkcja wykonywana przez proces potomny.
    Odbiera listę liczb, oblicza sumę i średnią, a następnie wysyła wyniki z powrotem.

    :param conn: Połączenie Pipe do komunikacji z procesem nadrzędnym.
    """
    # Odbieramy listę liczb od procesu nadrzędnego
    numbers: List[int] = conn.recv()
    # Obliczamy sumę i średnią
    total: int = sum(numbers)
    average: float = total / len(numbers) if numbers else 0.0
    # Wysyłamy wyniki z powrotem do procesu nadrzędnego
    conn.send((total, average))
    # Zamykamy połączenie
    conn.close()


def main() -> None:
    """
    Funkcja główna - tworzy proces potomny i zarządza komunikacją.
    """
    parent_conn, child_conn = Pipe()
    p = Process(target=child_process, args=(child_conn,))
    p.start()

    # Lista liczb do wysłania do procesu potomnego
    numbers: List[int] = [1, 2, 3, 4, 5]
    # Wysyłamy listę liczb do procesu potomnego
    parent_conn.send(numbers)
    # Odbieramy wyniki od procesu potomnego
    total, average = parent_conn.recv()
    # Czekamy na zakończenie procesu potomnego
    p.join()

    # Drukujemy wyniki
    print(f"Suma: {total}, Średnia: {average:.2f}")


if __name__ == "__main__":
    main()
