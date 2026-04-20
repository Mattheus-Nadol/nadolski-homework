import threading
import time

def jakis_program(numer):
    print(f"Jestem wątkiem numer: {numer}.")

print("Główny program czeka na zakończenie...")
watki = []
for i in range(1, 6):
    thread = threading.Thread(target=jakis_program, args=(i,))
    time.sleep(1)
    watki.append(thread)
    thread.start()

for thread in watki:
    thread.join()

print("Zakonczono")
