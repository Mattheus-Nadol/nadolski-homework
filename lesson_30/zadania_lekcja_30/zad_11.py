import threading
import queue
import time
import random

# Tworzymy bezpieczną wątkowo kolejkę
q = queue.Queue()

# Flaga do zatrzymania wątków po 10 sekundach
stop_flag = False

# Funkcja producenta
def producent():
    while not stop_flag:
        liczba = random.randint(1, 100)
        q.put(liczba)
        print(f"Producent dodał: {liczba}")
        time.sleep(1)  # co 1 sekundę dodaje nowy element

# Funkcja konsumenta
def konsument():
    while not stop_flag or not q.empty():  # dopóki nie minęło 10s lub kolejka nie jest pusta
        try:
            liczba = q.get(timeout=0.5)  # czekamy maks 0.5s na element
            print(f"Konsument pobrał: {liczba}")
        except queue.Empty:
            continue
        time.sleep(1.5)  # co 1.5 sekundy pobiera element

if __name__ == "__main__":
    # Tworzymy wątki
    t1 = threading.Thread(target=producent)
    t2 = threading.Thread(target=konsument)

    t1.start()
    t2.start()

    # Program działa 10 sekund
    time.sleep(10)
    stop_flag = True

    # Czekamy na zakończenie wątków
    t1.join()
    t2.join()

    print("Program zakończony.")