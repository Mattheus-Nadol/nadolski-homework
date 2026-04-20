import threading

# Dane
lista = list(range(10_000_000))

suma_calkowita = 0
lock = threading.Lock()

def sumuj_fragment(fragment):
    global suma_calkowita
    suma_czesciowa = sum(fragment)

    # sekcja krytyczna
    with lock:
        suma_calkowita += suma_czesciowa

# Podział listy na 4 części
rozmiar = len(lista) // 4
fragmenty = [
    lista[0:rozmiar], # elementy 0 do 2_499_999
    lista[rozmiar:2*rozmiar], # 2_500_000 do 4_999_999
    lista[2*rozmiar:3*rozmiar], # 5_000_000 do 7_499_999
    lista[3*rozmiar:] # pozostale
]

watki = []

for fragment in fragmenty:
    t = threading.Thread(target=sumuj_fragment, args=(fragment,))
    watki.append(t)
    t.start()

for t in watki:
    t.join()

print("Suma całkowita:", suma_calkowita)
print("Suma kontrolna:", sum(lista))