import threading

lista = []
lock = threading.Lock()

def dodaj_jedynki():
    for _ in range(100_000):
        with lock:
            lista.append(1)

def dodaj_dwojki():
    for _ in range(100_000):
        with lock:
            lista.append(2)

t1 = threading.Thread(target=dodaj_jedynki)
t2 = threading.Thread(target=dodaj_dwojki)

t1.start()
t2.start()

t1.join()
t2.join()

print("Długość listy:", len(lista))