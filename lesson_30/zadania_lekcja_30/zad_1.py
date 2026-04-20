import threading
import time

def jakis_program():
    time.sleep(3)
    print("Wątek zakończył pracę")

thread = threading.Thread(target=jakis_program)

thread.start()
print("Główny program czeka na wątek...")
thread.join()
