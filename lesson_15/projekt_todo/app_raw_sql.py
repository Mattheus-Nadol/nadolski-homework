# app_raw_sql.py
"""
Aplikacja konsolowa do zarządzania zadaniami.

Komunikuje się z modułem bazy danych w celu wyświetlania, dodawania
i aktualizacji zadań. Udostępnia prosty interfejs menu do obsługi
interakcji z użytkownikiem.
"""
import database_raw as db

class TaskApp:
    """Klasa obsługująca interfejs aplikacji konsolowej do zarządzania zadaniami."""
    def __init__(self):
        """
        Inicjalizuje aplikację z obiektem TaskManagerRaw.
        :param manager: Instancja klasy TaskManagerRaw do operacji na bazie.
        """
        self.manager = db.TaskManagerRaw()

    def pokaz_zadania(self):
        """Wyświetla listę wszystkich zadań."""
        zadania = self.manager.pobierz_zadania()
        if not zadania:
            print("Brak zadań na liście.")
            return

        print("\n--- Twoja lista zadań ---")
        for zadanie in zadania:
            status = "✓" if zadanie[2] else "✗"
            print(f"[{status}] ID: {zadanie[0]}, Opis: {zadanie[1]}, Priorytet: {zadanie[3]}")
        print("------------------------\n")

    def pokaz_zadania_fraza(self, fraza):
        """Wyszukuje po frazie"""
        zadania = self.manager.wyszukaj_zadania(fraza)
        if not zadania:
            print(f"Brak zadań z podaną frazą '{fraza}'.")
            return

        print(f"\n--- Twoja lista zadań z frazą '{fraza}'---")
        for zadanie in zadania:
            status = "✓" if zadanie[2] else "✗"
            print(f"[{status}] ID: {zadanie[0]}, Opis: {zadanie[1]}, Priorytet: {zadanie[3]}")
        print("------------------------\n")

    def run(self):
        """
        Funkcja główna aplikacji.
        
        Uruchamia menu konsolowe, pozwalające użytkownikowi na przeglądanie,
        dodawanie oraz aktualizowanie zadań w bazie danych. Obsługuje interakcję
        z użytkownikiem w pętli do momentu wyjścia z programu.
        """

        while True:
            print("Menu:")
            print("1. Pokaż zadania")
            print("2. Dodaj zadanie")
            print("3. Oznacz zadanie jako zrobione")
            print("4. Wyszukaj zadanie")
            print("5. Usuń zadanie")
            print("6. Wyjdź")

            wybor = input("Wybierz opcję: ")

            if wybor == '1':
                self.pokaz_zadania()
            elif wybor == '2':
                opis = input("Podaj opis zadania: ")
                priorytet = input("Podaj priorytet (1-3): ")
                self.manager.dodaj_zadanie(opis, priorytet)
                print("Zadanie dodane!")
            elif wybor == '3':
                try:
                    id_zadania = int(input("Podaj ID zadania do oznaczenia: "))
                    self.manager.oznacz_jako_zrobione(id_zadania)
                    print("Zadanie zaktualizowane!")
                except ValueError:
                    print("Błędne ID. Podaj liczbę.")
            elif wybor == '4':
                fraza = input("Podaj frazę do wyszukania zadania: ")
                self.pokaz_zadania_fraza(fraza)
            elif wybor == '5':
                try:
                    id_zadania = int(input("Podaj ID zadania do usunięcia: "))
                    self.manager.usun_zadanie(id_zadania)
                    print("Zadanie usunięte")
                except ValueError:
                    print("Błędne ID. Podaj liczbę.")
            elif wybor == '6':
                print("Do zobaczenia!")
                break
            else:
                print("Nieznana opcja, spróbuj ponownie.")

if __name__ == "__main__":
    app = TaskApp()
    app.run()
