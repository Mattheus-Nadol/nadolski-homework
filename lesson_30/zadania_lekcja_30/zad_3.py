import threading
import time

def pobierz_dane(id_danych):
    time.sleep(2)
    print(f"ID: {id_danych}.")

# watkowo
watki = []
start_time = time.time()

for i in range(3):
    thread = threading.Thread(target=pobierz_dane, args=(i,))
    watki.append(thread)
    thread.start()

for thread in watki:
    thread.join()

print(f"Czas: {time.time() - start_time:.2f}")

# sekwencyjnie
start_time2 = time.time()

for i in range(3, 6):
    pobierz_dane(i)

print(f"Czas sekwencyjnie: {time.time() - start_time2:.2f}")