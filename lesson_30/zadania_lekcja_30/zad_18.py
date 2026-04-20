"""
Zadanie 18: Wątki i synchronizacja - Konto bankowe

Ten moduł demonstruje użycie wątków oraz synchronizacji za pomocą threading.Lock
na przykładzie prostego konta bankowego.

Źródła i dokumentacja:
- threading: https://docs.python.org/3/library/threading.html
- random: https://docs.python.org/3/library/random.html
"""

import threading
import random

class KontoBankowe:
    """
    Klasa reprezentująca konto bankowe z bezpiecznymi metodami wpłaty i wypłaty.
    """
    def __init__(self, saldo_poczatkowe: float = 0.0) -> None:
        self.saldo: float = saldo_poczatkowe
        self._lock = threading.Lock()

    def wplac(self, kwota: float) -> None:
        """
        Wpłaca podaną kwotę na konto w sposób bezpieczny dla wątków.
        """
        with self._lock:
            self.saldo += kwota
            print(f"Wpłacono {kwota:.2f}, nowe saldo: {self.saldo:.2f}")

    def wyplac(self, kwota: float) -> None:
        """
        Wypłaca podaną kwotę z konta w sposób bezpieczny dla wątków.
        Jeżeli saldo jest niewystarczające, wypłata nie jest realizowana.
        """
        with self._lock:
            if self.saldo >= kwota:
                self.saldo -= kwota
                print(f"Wypłacono {kwota:.2f}, nowe saldo: {self.saldo:.2f}")
            else:
                print(f"Brak środków na wypłatę {kwota:.2f}. Saldo: {self.saldo:.2f}")
                pass

def zadanie_18() -> None:
    """
    Funkcja uruchamiająca testowe wpłaty i wypłaty na koncie bankowym za pomocą wątków.
    """
    konto = KontoBankowe(1000.0)  # saldo początkowe
    watki = []

    # Funkcje do uruchomienia w wątkach
    def wplata():
        kwota = random.uniform(50, 200)
        konto.wplac(kwota)

    def wyplata():
        kwota = random.uniform(50, 200)
        konto.wyplac(kwota)

    # Tworzymy 5 wątków wpłacających i 5 wypłacających
    for _ in range(5):
        watki.append(threading.Thread(target=wplata))
        watki.append(threading.Thread(target=wyplata))

    # Uruchamiamy wszystkie wątki
    for w in watki:
        w.start()

    # Czekamy na zakończenie wszystkich wątków
    for w in watki:
        w.join()

    print(f"Saldo końcowe: {konto.saldo:.2f}")

if __name__ == "__main__":
    zadanie_18()