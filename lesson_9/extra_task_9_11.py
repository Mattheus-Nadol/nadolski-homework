#11. Do programu kalkulator (z lekcji 8 zad 1),
# dodaj funkcje zapisywania i odczytywania danych z pliku lub plików (jeżeli widzisz potrzebe).

from typing import Union
import csv
from pathlib import Path

class WrongOperatorError(Exception):
    """Utworzony błąd dla błędnej operacji."""

def calculator(a: Union[int, float], b: Union[int,float], operation: str) -> float:
    """Działanie matematyczne dla dwóch liczb z wyborem rodzaju działania.
    
    Funkcja przyjmuje dwie liczby i string z operacją ("+", "-", "*" lub "/"),
    a następie zwraca wynik odpowiedniego działania.

    :param a: Pierwsza liczba (liczba całkowita lub zmiennoprzecinkowa).
    :param b: Druga liczba (liczba całkowita lub zmiennoprzecinkowa).
    :param operation: Symbol operacji matematycznej (string).
    :return: wynik działania matematycznego.
    """
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        if b == 0:
            raise ZeroDivisionError
        return a / b
    else:
        # If none of the recognized operations matched, raise a clear error.
        raise WrongOperatorError("Błędny operator")

def save_to_file(a, op, b, result):
    """Zapisywanie do pliku"""
    file_path = Path("calc_log.csv")
    file_exists = file_path.exists()
    with open("calc_log.csv", "a", newline="", encoding="utf-8") as file:
        log_header = ["A", "Działanie", "B", "Wynik"]
        file_writer = csv.DictWriter(file, fieldnames=log_header, delimiter=';')
        if not file_exists:
            file_writer.writeheader()     # first row = header if file not exists
        file_writer.writerow({
                "A": a,
                "Działanie": op,
                "B": b,
                "Wynik": result,
        })      # rest = data rows

def read_from_file():
    """Czytanie z pliku"""
    try:
        with open("calc_log.csv", "r", encoding="utf-8") as file:
            file_reader = csv.DictReader(file, delimiter=';')
            # Then iterate over the remaining lines
            for i, row in enumerate(file_reader, start=1):
                print(f'{i}. {row["A"]} {row["Działanie"]} {row["B"]} = {row["Wynik"]}')
    except FileNotFoundError as e:
        print(f"Plik nie istnieje - błąd: {e}")

while True:
    user_choice = input("1 - Oblicz i zapisz, 2 - Historia zapisanych obliczeń, Z - Zakończ: ")

    if user_choice == "1":
        try:
            a_input = float(input("Podaj liczbę A: "))
            b_input = float(input("Podaj liczbę B: "))
            op_input = str(input("Podaj operację: "))
            input_result = calculator(a_input, b_input, op_input)
        except ValueError:
            print("Podane wartości nie są liczbami")
        except ZeroDivisionError:
            print("Nie dzielimy przez zero")
        except WrongOperatorError:
            print("Błędny operator")
        else:
            print(f"Wynik działania to: {input_result}")
            save_to_file(a_input, op_input, b_input, input_result)

    elif user_choice == "2":
        read_from_file()

    else:
        break
