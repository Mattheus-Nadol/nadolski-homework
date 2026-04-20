"""Moduł do równoległej analizy sentymentu zdań za pomocą wątków.

Zawiera listę przykładowych zdań oraz funkcję analizującą sentyment każdego zdania
z użyciem ThreadPoolExecutor. Mierzy i wyświetla czas wykonania analizy.

Źródła i dokumentacja użytych bibliotek:
- concurrent.futures: https://docs.python.org/3/library/concurrent.futures.html
- random: https://docs.python.org/3/library/random.html
- time: https://docs.python.org/3/library/time.html

Sposób użycia ThreadPoolExecutor oraz symulacja czasu przetwarzania
zostały zaczerpnięte z dokumentacji concurrent.futures oraz standardowych przykładów
wielowątkowego przetwarzania w Pythonie. Symulacja czasu (time.sleep z losowym czasem)
ma na celu imitację rzeczywistego czasu obliczeń, co pozwala zobaczyć korzyści
z równoległego przetwarzania."""
  
import concurrent.futures
import random
import time
from typing import List, Tuple


# Lista 20 przykładowych zdań/opinii do analizy sentymentu
zdania: List[str] = [
    "To był niesamowity dzień pełen niespodzianek.",
    "Nie podobał mi się ten film, był nudny.",
    "Obsługa klienta była bardzo pomocna i uprzejma.",
    "Produkt nie spełnił moich oczekiwań.",
    "Uwielbiam tę restaurację, zawsze jest pyszne jedzenie.",
    "Ta książka była przeciętna, nic specjalnego.",
    "Jestem zadowolony z zakupu, wszystko działa jak należy.",
    "Nie polecam tego hotelu, warunki były kiepskie.",
    "Film miał świetną obsadę i ciekawą fabułę.",
    "Dostawa była opóźniona, ale produkt był dobry.",
    "Nie mam zdania na ten temat.",
    "Wspaniałe doświadczenie, na pewno wrócę.",
    "Jakość zdjęć jest słaba, rozczarowujące.",
    "Obsługa była szybka i efektywna.",
    "Nie podobała mi się muzyka na imprezie.",
    "To miejsce ma wyjątkowy klimat i atmosferę.",
    "Produkt jest przereklamowany i zbyt drogi.",
    "Bardzo polecam ten kurs, dużo się nauczyłem.",
    "Nie warto tracić czasu na ten serial.",
    "Świetna jakość i szybka realizacja zamówienia."
]


def analizuj_sentyment(zdanie: str) -> Tuple[str, str]:
    """
    Symuluje analizę sentymentu zdania.

    Losowo wybiera wynik analizy spośród "Pozytywny", "Negatywny", "Neutralny".
    Symuluje czas przetwarzania od 0.1 do 0.5 sekundy.

    Args:
        zdanie (str): Zdanie do analizy.

    Returns:
        Tuple[str, str]: Krotka zawierająca zdanie i wynik analizy sentymentu.
    """
    czas_przetwarzania = random.uniform(0.1, 0.5)
    time.sleep(czas_przetwarzania)
    wynik = random.choice(["Pozytywny", "Negatywny", "Neutralny"])
    return zdanie, wynik


def main() -> None:
    """
    Przeprowadza równoległą analizę sentymentu dla listy zdań.

    Używa ThreadPoolExecutor do równoległego przetwarzania,
    mierzy czas wykonania i drukuje wyniki.
    """
    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        wyniki = list(executor.map(analizuj_sentyment, zdania))

    koniec = time.perf_counter()
    print(f"Czas wykonania analizy: {koniec - start:.2f} sekund\n")

    for zdanie, sentyment in wyniki:
        print(f"Zdanie: {zdanie}\nSentyment: {sentyment}\n")


if __name__ == "__main__":
    main()
