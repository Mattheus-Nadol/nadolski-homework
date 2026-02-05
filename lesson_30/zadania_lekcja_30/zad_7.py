import multiprocessing

def potega(liczba, pot):
    wynik = liczba ** pot
    print(f"{liczba} do potęgi {pot} = {wynik}")

if __name__ == "__main__":
    proces = multiprocessing.Process(
        target=potega,
        args=(5, 3)
    )

    proces.start()
    proces.join()

    print("Proces główny zakończył działanie")