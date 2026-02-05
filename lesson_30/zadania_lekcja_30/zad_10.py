import threading
import os

# Funkcja licząca wystąpienia danego słowa w pliku
def licz_slowa(nazwa_pliku, szukane_slowo, wyniki, lock):
    with open(nazwa_pliku, 'r', encoding='utf-8') as f:
        tekst = f.read()
    # Liczymy wystąpienia słowa, ignorując wielkość liter
    liczba_wystapien = tekst.lower().split().count(szukane_slowo.lower())
    with lock:
        wyniki[nazwa_pliku] = liczba_wystapien

if __name__ == "__main__":
    katalog = "./pliki"  # podaj ścieżkę do katalogu z plikami
    pliki = [os.path.join(katalog, f) for f in os.listdir(katalog) if f.endswith(".txt")]

    szukane_slowo = input("Podaj słowo do zliczenia: ")

    wyniki = {}
    lock = threading.Lock()
    watki = []

    for plik in pliki:
        t = threading.Thread(target=licz_slowa, args=(plik, szukane_slowo, wyniki, lock))
        watki.append(t)
        t.start()

    for t in watki:
        t.join()

    laczna_liczba = sum(wyniki.values())
    print("Wyniki liczenia słowa w plikach:")
    for plik, liczba in wyniki.items():
        print(f"{plik}: {liczba} wystąpień")
    print(f"Łączna liczba wystąpień słowa '{szukane_slowo}': {laczna_liczba}")