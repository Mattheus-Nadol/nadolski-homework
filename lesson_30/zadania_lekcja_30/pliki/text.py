import random

# Przykładowe słowa
slowa = [
    "kot", "pies", "dom", "drzewo", "samochód", "rower", "komputer", "telefon",
    "kawa", "herbata", "książka", "stół", "krzesło", "okno", "drzwi", "słońce",
    "księżyc", "gwiazda", "chleb", "masło", "ser", "jajko", "woda", "sok",
    "lampa", "telefon", "długopis", "papier", "notatnik", "plecak", "torba",
    "buty", "czapka", "rękawiczki", "szalik", "spodnie", "koszula", "bluza",
    "miasto", "wieś", "droga", "ulica", "park", "ogród", "jezioro", "rzeka",
    "morze", "góra", "las", "zwierzę", "owoc", "warzywo", "samolot", "pociąg"
]

# Tworzymy losowy tekst z 200 słów
random_slowa = [random.choice(slowa) for _ in range(200)]

# Zapis do pliku txt
with open("slowa_testowe.txt", "w", encoding="utf-8") as f:
    for slowo in random_slowa:
        f.write(slowo + "\n")