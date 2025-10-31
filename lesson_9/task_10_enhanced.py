#10+. Mini-projekt: Lista zadań:
import json

def load_from_file(file_name):
    """Funkcja próbuje załadować plik 'zadania.json' a następnie wyświetla zawartość
    (jeśli nie napotka błędu)"""
    try:
        if file_name.endswith(".json"):
            with open(file_name, "r", encoding="utf-8") as file:
                content = file.read()
                if not content:
                    print("Plik jest pusty")
                    return
                file_data = json.loads(content)
                if isinstance(file_data, dict):
                    if not file_data:
                        print("Plik nie zawiera żadnych zadań")
                    else:
                        task_list.update(file_data)
                        print("Dane z pliku", file_data)   
                else:
                    print("Plik zawiera niepoprawny format danych")
        else:
            print("Plik nie jest w formacie json")            
    except FileNotFoundError as e:
        print(f"Plik nie istnieje - błąd: {e}")
    except json.decoder.JSONDecodeError as j:
        print(f"Plik jest uszkodzony - błąd: {j}")


def create_task():
    """Funkcja tworzy nowe zdanie podane przez użytkownika do listy 'task_list' (dict),
    w formie "numer"(key):"zadanie"(value)
    Jeśli jest pusta - numer zadania to "1", jeśli nie, zwiększa następny numer o 1
    (poprzez sprawdzenie ilości kluczy zawartych już w słowniku)
    """
    task_number = 1
    user_task = input("Jakie zadanie chcesz dodać: ")
    while not user_task.strip():
        user_task = input("Wpisałeś pustą wartość - wpisz ponownie")
    if task_list:
        task_number = len(task_list) + 1
    task_list.update({task_number:user_task.title()})

def show_tasks():
    """Funkcja wyświetla wszystkie zadania"""
    if not task_list:
        print("Brak zadań w liście")
    else:    
        print("Lista zadań: ")
        for number, task in task_list.items():
            print(f"{number}. {task}")

def add_to_file():
    """Funkcja zapisuje do pliku listę zadań dodanych w funkcji "create_task()".
    Jeśli dostępna lista zadań task_list (dict) jest pusta - wyświetla komunikat.
    Jeśli zawiera zadania - dodaje je do pliku."""
    try:
        with open("zadania.json", "w", encoding="utf-8") as file:
            if not task_list:
                print("Lista jest pusta, nie ma co dodawać!")
            else:    
                json.dump(task_list, file, indent=4, ensure_ascii=False)
                print("Pomyślnie zapisano zadania do pliku!")
    except OSError as e:
        print(f"Błąd zapisu: {e}")

task_list:dict = {}
while True:
    user_choice = input("1 - załaduj plik, 2 - utwórz zadanie, 3 - dodaj do pliku, " \
    "4 - wyświetl zawartość, 5 - zakończ program i dodaj do pliku: ")
    if user_choice == "1":
        user_file = input("Podaj nazwę pliku (domyślnie 'zadania.json'): ") or "zadania.json"
        load_from_file(user_file)
    elif user_choice == "2":
        create_task()
    elif user_choice == "3":
        add_to_file()
    elif user_choice == "4":
        show_tasks()
    elif user_choice == "5":
        add_to_file()
        print("Dodano zadania, zakończenie programu.")
        break
    else:
        print("Wrong choice")
