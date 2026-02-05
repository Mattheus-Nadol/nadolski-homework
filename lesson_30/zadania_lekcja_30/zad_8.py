"""
Uwaga: Zgodnie z treścią zadania, input() powinien być wykonywany w procesie
potomnym. Na systemach macOS i Windows powoduje to jednak błąd EOFError,
ponieważ proces potomny nie ma dostępu do stdin.

Dlatego pobieranie danych od użytkownika odbywa się w procesie głównym,
a komunikacja między procesami jest realizowana za pomocą multiprocessing.Queue.
"""
import multiprocessing

def przywitanie(imie, kolejka):
    kolejka.put(f"Witaj, {imie}!")

if __name__ == "__main__":
    imie = input("Podaj swoje imię: ")

    kolejka = multiprocessing.Queue()

    proces = multiprocessing.Process(
        target=przywitanie,
        args=(imie, kolejka)
    )

    proces.start()

    komunikat = kolejka.get()
    proces.join()

    print(komunikat)