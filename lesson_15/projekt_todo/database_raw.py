# database_raw.py
"""
Moduł do zarządzania zadaniami w bazie danych SQLite.

Zawiera funkcje do inicjalizacji bazy danych, dodawania zadań,
pobierania listy zadań oraz oznaczania ich jako wykonane.
Wykorzystuje surowe zapytania SQL z podstawianiem parametrów,
aby zapobiec atakom typu SQL Injection.
"""
import sqlite3

class TaskManagerRaw:
    """
    Klasa do zarządzania zadaniami w bazie SQLite przy użyciu surowych zapytań SQL.
    """
    def __init__(self, db_name: str = 'todo_raw.db'):
        """Inicjalizuje bazę danych i tworzy tabelę, jeśli nie istnieje."""
        self.db_name = db_name
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Używamy IF NOT EXISTS, aby uniknąć błędu przy ponownym uruchomieniu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS zadania (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    opis TEXT NOT NULL,
                    priorytet INTEGER DEFAULT 1,
                    zrobione BOOLEAN NOT NULL CHECK (zrobione IN (0, 1))
                )
            ''')
            conn.commit()

    def dodaj_zadanie(self, opis: str, priorytet: int):
        """Dodaje nowe zadanie do bazy danych."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Używamy placeholderów (?), aby zapobiec SQL Injection
            cursor.execute("INSERT INTO zadania (opis, priorytet, zrobione) VALUES (?, ?, ?)",
                           (opis, priorytet, False))
            conn.commit()

    def pobierz_zadania(self) -> list[tuple]:
        """Pobiera wszystkie zadania z bazy danych."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, opis, zrobione, priorytet FROM zadania")
            return cursor.fetchall()

    def wyszukaj_zadania(self, fraza: str) -> list:
        """Wyszukuje zadania z bazy danych, zawierające daną frazę."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, opis, zrobione, priorytet FROM zadania WHERE opis LIKE ?",
                           (f"%{fraza}%",))
            return cursor.fetchall()

    def oznacz_jako_zrobione(self, id_zadania: int):
        """Oznacza zadanie o podanym ID jako zrobione."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE zadania SET zrobione = ? WHERE id = ?",
                           (True, id_zadania))
            conn.commit()

    def usun_zadanie(self, id_zadania: int):
        """Usuwa zadanie o podanym ID."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM zadania WHERE id = ?",
                           (id_zadania,))
            conn.commit()
