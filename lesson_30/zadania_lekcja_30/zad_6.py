import multiprocessing
import math

def oblicz_silnie():
    wynik = math.factorial(10)
    print("Silnia 10 =", wynik)

if __name__ == "__main__": # OBOWIĄZKOWE przy multiprocessing
    proces = multiprocessing.Process(target=oblicz_silnie)
    
    proces.start()   # uruchamiamy proces
    proces.join()    # czekamy aż się zakończy

    print("Proces główny zakończył działanie")