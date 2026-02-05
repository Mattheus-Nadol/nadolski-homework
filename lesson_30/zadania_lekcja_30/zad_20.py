"""
Zadanie 20 - Przetwarzanie równoległe obrazów (CPU-bound) w Pythonie

Program generuje 10 "obrazów" jako listy 1000x1000 losowych liczb i przetwarza je sekwencyjnie oraz równolegle
przy użyciu multiprocessing.Pool. Przetwarzanie polega na przemnożeniu każdego "piksela" przez 1.1.

Źródła i dokumentacja:
- https://docs.python.org/3/library/multiprocessing.html
- https://realpython.com/python-multiprocessing/
- https://docs.python.org/3/library/random.html
"""

import random
import time
from multiprocessing import Pool, cpu_count

def generuj_obraz(rozmiar=1000):
    """
    Generuje "obraz" jako listę list losowych liczb zmiennoprzecinkowych.
    :param rozmiar: liczba wierszy i kolumn obrazu
    :return: lista list floatów
    """
    return [[random.random() for _ in range(rozmiar)] for _ in range(rozmiar)]

def zastosuj_filtr(obraz):
    """
    Przetwarza obraz mnożąc każdy piksel przez 1.1.
    :param obraz: lista list floatów
    :return: przetworzony obraz (lista list floatów)
    """
    # Symulacja kosztownej operacji CPU-bound na każdym pikselu
    return [[piksel * 1.1 for piksel in wiersz] for wiersz in obraz]

def main():
    # Parametry
    liczba_obrazow = 10
    rozmiar_obrazow = 1000

    # Generowanie obrazów
    obrazy = [generuj_obraz(rozmiar_obrazow) for _ in range(liczba_obrazow)]

    # Przetwarzanie sekwencyjne
    t0 = time.time()
    wyniki_sekwencyjne = [zastosuj_filtr(obraz) for obraz in obrazy]
    t1 = time.time()
    print(f"Czas przetwarzania sekwencyjnego: {t1 - t0:.2f} s")

    # Przetwarzanie równoległe
    t2 = time.time()
    with Pool(processes=cpu_count()) as pool:
        wyniki_rownolegle = pool.map(zastosuj_filtr, obrazy)
    t3 = time.time()
    print(f"Czas przetwarzania równoległego: {t3 - t2:.2f} s")

    # Komentarz wyjaśniający:
    # Równoległe przetwarzanie czasem zajmuje więcej czasu, bo trzeba najpierw przygotować i uruchomić kilka procesów,
    # a potem przesłać do nich duże dane (obrazy). To zajmuje chwilę i może "zjeść" czas, który oszczędzamy na
    # równoczesnej pracy. Dlatego, jeśli zadanie nie jest bardzo trudne albo dane są bardzo duże, czasem lepiej zrobić
    # wszystko po kolei. Warto więc zawsze sprawdzić, co jest szybsze w danym przypadku.

if __name__ == "__main__":
    main()