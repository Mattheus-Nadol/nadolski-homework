# sqlalchemy_app/app_orm.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from sqlalchemy_app.database import get_db
from sqlalchemy_app.models import Zadanie, Tag


def pokaz_zadania(db: Session):
    """Wyświetla listę wszystkich zadań."""
    zadania = db.query(Zadanie).all() # Zamiast SELECT * FROM ...
    if not zadania:
        print("Brak zadań na liście.")
        return

    print("\n--- Twoja lista zadań ---")
    for zadanie in zadania:
        status = "✓" if zadanie.zrobione else "✗"
        # Pobieramy listę tagów przypisanych do zadania
        tag_list = ", ".join([tag.nazwa for tag in zadanie.tagi]) if zadanie.tagi else "brak"
        print(f"[{status}] ID: {zadanie.id}, Opis: {zadanie.opis}, Tagi: {tag_list}, Data: {zadanie.data_utworzenia}")
    print("------------------------\n")

def dodaj_zadanie(db: Session, opis: str):
    """Dodaje nowe zadanie do bazy."""
    nowe_zadanie = Zadanie(opis=opis) # Tworzymy obiekt, a nie piszemy INSERT
    db.add(nowe_zadanie)
    db.commit()
    db.refresh(nowe_zadanie) # Odśwież, aby pobrać ID

def oznacz_jako_zrobione(db: Session, id_zadania: int):
    """Oznacza zadanie jako zrobione."""
    zadanie = db.query(Zadanie).filter(Zadanie.id == id_zadania).first() # Wyszukujemy obiekt
    if zadanie:
        zadanie.zrobione = True #type: ignore # Po prostu zmieniamy atrybut!
        db.commit()
        print("Zadanie zaktualizowane!")
    else:
        print("Nie znaleziono zadania o podanym ID.")

# def usun_zadanie(db: Session, id_zadania: int):
#     print("Przed usuwaniem - jestem tu")
#     result = db.query(Zadanie).filter(Zadanie.id == id_zadania)
#     print(result) # jak SELECT w SQL

def usun_zadanie(db: Session, id_zadania: int):
    """Usuwa zadanie"""
    zadanie = db.query(Zadanie).filter(Zadanie.id == id_zadania).first()
    if zadanie:
        db.delete(zadanie)
        db.commit()
        print("Zadanie usunięte!")
    else:
        print("Nie znaleziono zadania o podanym ID.")

def wyszukaj_zadanie(db: Session, fraza: str):
    """Wyszukuje zadanie po wybranej frazie"""
    zadania = db.query(Zadanie).filter(Zadanie.opis.contains(fraza)).all() # Wyszukujemy obiekt
    if not zadania:
        print(f"Brak zadań z podaną frazą '{fraza}'.")
        return

    print(f"\n--- Twoja lista zadań z frazą '{fraza}'---")
    for zadanie in zadania:
        status = "✓" if zadanie.zrobione else "✗"
        print(f"[{status}] ID: {zadanie.id}, Opis: {zadanie.opis}, Data: {zadanie.data_utworzenia}")
    print("------------------------\n")


def dodaj_tag_do_zadania(db: Session, id_zadania: int, nazwa_taga: str):
    """Dodaje tag do zadania"""
    zadanie = db.query(Zadanie).filter(Zadanie.id == id_zadania).first()
    if not zadanie:
        print("Nie znaleziono zadania.")
        return
    tag = db.query(Tag).filter(Tag.nazwa == nazwa_taga).first()
    if not tag:
        tag = Tag(nazwa=nazwa_taga)
        db.add(tag)
    zadanie.tagi.append(tag)
    db.commit()
    print(f"Tag '{nazwa_taga}' dodany do zadania ID {id_zadania}.")


def edytuj_zadanie(db: Session, id_zadania: int):
    """Edytuje treść zadania"""
    zadanie = db.query(Zadanie).filter(Zadanie.id == id_zadania).first()

    if not zadanie:
        print("Nie znaleziono zadania o podanym ID.")
        return

    nowy_opis = ""
    while not nowy_opis.strip():
        nowy_opis = input("Podaj nowy opis (nie może być pusty): ")

    zadanie.opis = nowy_opis #type: ignore
    db.commit()
    print("Zadanie zaktualizowane!")


def main():
    """Główna funkcja aplikacji"""
    db_generator = get_db()
    db_session = next(db_generator)
    while True:
        print("Menu (SQLAlchemy):")
        print("1. Pokaż zadania")
        print("2. Dodaj zadanie")
        print("3. Edytuj treść zadania")
        print("4. Oznacz zadanie jako zrobione")
        print("5. Wyszukaj zadanie po frazie")
        print("6. Dodaj tag do zadania")
        print("7. Usuwanie zadania")
        print("8. Wyjdź")

        wybor = input("Wybierz opcję: ")

        if wybor == '1':
            pokaz_zadania(db_session)
        elif wybor == '2':
            opis = input("Podaj opis zadania: ")
            dodaj_zadanie(db_session, opis)
            print("Zadanie dodane!")
        elif wybor == '3':
            try:
                id_zadania = int(input("Podaj ID zadania do edycji: "))
                edytuj_zadanie(db_session, id_zadania)
            except ValueError:
                print("Błędne ID. Podaj liczbę.")
        elif wybor == '4':
            try:
                id_zadania = int(input("Podaj ID zadania do oznaczenia: "))
                oznacz_jako_zrobione(db_session, id_zadania)
            except ValueError:
                print("Błędne ID. Podaj liczbę.")
        elif wybor == '5':
            fraza = input("Podaj frazę do wyszukania zadania: ")
            wyszukaj_zadanie(db_session, fraza)
        elif wybor == '6':
            nazwa_taga = input("Podaj nazwę taga: ")
            try:
                id_zadania = int(input("Podaj ID zadania: "))
                dodaj_tag_do_zadania(db_session, id_zadania, nazwa_taga)
            except ValueError:
                print("Błędne ID. Podaj liczbę.")
        elif wybor == '7':
            try:
                id_zadania = int(input("Podaj ID zadania do usunięcia: "))
                usun_zadanie(db_session, id_zadania)
            except ValueError:
                print("Błędne ID. Podaj liczbę.")
        elif wybor == '8':
            print("Do zobaczenia!")
            db_session.close()
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")

if __name__ == "__main__":
    main()
