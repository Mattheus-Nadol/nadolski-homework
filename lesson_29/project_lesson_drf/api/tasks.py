# my_app/tasks.py
import csv
import os
import time
from datetime import timedelta, datetime
import random

from celery import shared_task
import requests
from bs4 import BeautifulSoup
from PIL import Image # Importujemy Pillow do otwarcia pliku

from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from .models import EmailNotification, LogEntry, PageTitle, UploadedImage

# Używamy dekoratora @shared_task, aby zadanie było dostępne
# w całej aplikacji, bez potrzeby bezpośredniego importowania instancji
# Celery.

@shared_task
def add(x, y):
    """Proste zadanie, które dodaje dwie liczby."""
    return x + y

@shared_task
def simulate_cpu_bound_task(duration):
    """
    Symuluje długotrwałe zadanie CPU-bound, np. generowanie raportu.
    Używamy time.sleep(), aby zasymulować opóźnienie.
    """
    print(f"Rozpoczynam zadanie, które potrwa {duration} sekund...")
    time.sleep(duration)
    print("Zadanie zakończone.")
    return f"Raport wygenerowany pomyślnie po {duration} sekundach."

# (29) Zadanie 10 & (29) Zadanie 18 (priority queue)
@shared_task(queue="priority_queue")
def send_welcome_email(notification_id):
    """
    Symuluje wysyłkę maila na podstawie EmailNotification ID
    i po zakończeniu ustawia sent_at.
    """
    notification = EmailNotification.objects.get(id=notification_id)

    # symulacja wysyłki maila
    print(f"Wysyłanie maila do {notification.recipient_email}...")
    time.sleep(10)
    print("Mail wysłany.")

    # aktualizacja sent_at
    notification.sent_at = timezone.now()
    notification.save(update_fields=["sent_at"])

    return f"Mail do {notification.recipient_email} wysłany i zapisany w bazie."

@shared_task
def send_periodic_summary(user_emails):
    print(f"Wysyłanie podsumowania do {len(user_emails)} użytkowników...")
    # Tutaj logika wysyłania maili
    print("Podsumowanie wysłane.")

@shared_task
def cleanup_old_logs():
    print("Rozpoczynam czyszczenie starych logów...")
    # Tutaj logika usuwania starych wpisów z bazy danych
    print("Logi wyczyszczone.")

# (29) Zadanie 1
@shared_task
def hello_world_task():
    print("Hello from Celery!")

# (29) Zadanie 2 (formularz w Swagger?)
@shared_task
def multiply(a, b):
    """Zadanie mnożące dwie liczby."""
    print(f"Wynik mnożenia: {a * b}")
    return a * b

# (29) Zadanie 3
@shared_task
def log_timestamp():
    """Zadanie zapisujące aktualną datę i godzinę do pliku log.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(f"{timestamp}\n")
    return f"Timestamp {timestamp} zapisany do log.txt"

# (29) Zadanie 5
@shared_task
def count_users():
    User = get_user_model()
    total = User.objects.count()
    print(f"Liczba użytkowników: {total}")
    return total

# (29) Zadanie 7
@shared_task
def update_user_last_login(user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])
    return f"Zaktualizowano last_login dla user_id={user_id}"

# (29) Zadanie 8
@shared_task
def process_video():
    time.sleep(15)
    print("Przetwarzanie wideo zakończone")

# (29) Zadanie 11
@shared_task(bind=True)
def long_running_task(self):
    total = 100
    for i in range(1, total + 1):
        time.sleep(0.1)
        self.update_state(state='PROGRESS', meta={'current': i, 'total': total})
    return {'current': total, 'total': total, 'status': 'Done'}

# (29) Zadanie 12
@shared_task
def cleanup_old_log_entries():
    # granica: 90 dni wstecz
    cutoff = timezone.now() - timedelta(days=90)
     # usuwamy stare wpisy
    deleted, _ = LogEntry.objects.filter(created_at__lt=cutoff).delete() # "_" to słownik z liczbą usuniętych obiektów per model - nie potrzebne
    return f"Usunięto {deleted} wpisów starszych niż 90 dni."

# (29) Zadanie 13
@shared_task
def fetch_example_title():
    """
    Pobiera tytuł strony example.com i zapisuje go do bazy,
    dlatego tworzymy model PageTitle jako miejsce trwałego zapisu.
    """
    url = "https://example.com" # strona do pobrania
    # pobieramy HTML
    response = requests.get(url, timeout=10) # obiekt odpowiedzi HTTP (status, treść strony itd.).
    response.raise_for_status() # podniesie błąd, jeśli status nie jest 200 OK

    # parsujemy HTML i wyciągamy tytuł
    soup = BeautifulSoup(response.text, "html.parser") # obiekt BeautifulSoup, czyli sparsowany HTML
                                                        # response.text — treść HTML jako string.
    title = soup.title.string.strip() if soup.title and soup.title.string else "Brak tytułu"
    # - title — wyciągnięty tytuł strony (albo fallback „Brak tytułu”).
    # - soup.title — znacznik <title> z HTML.
    # - .string — sam tekst tytułu.
    # - .strip() — usuwa spacje z początku/końca.

    # zapis do bazy - url i title trafiają do nowego rekordu.
    PageTitle.objects.create(url=url, title=title)
    return f"Pobrano tytuł: {title}"

# (29) Zadanie 14
@shared_task
def generate_users_csv():
    """
    Generuje CSV z użytkownikami i zapisuje go w katalogu media.
    Zwraca ścieżkę względną do pliku.
    """
    User = get_user_model()
    filename = f"users_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    rel_path = os.path.join("reports", filename)
    abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)

    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    with open(abs_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "email"])
        for user in User.objects.all():
            writer.writerow([user.username, user.email])

    return {"file_path": rel_path}

# (29) Zadanie 15
@shared_task(bind=True)
def retry_failing_request(self):
    url = "http://nonexistent.example.invalid"  # celowo nieistniejący adres
    try:
        requests.get(url, timeout=5)
    except Exception as exc:
        # ponów próbę 3 razy co 60 sekund
        raise self.retry(exc=exc, countdown=60, max_retries=3)

# (29) Zadanie 16
@shared_task
def classify_image(image_id):
    obj = UploadedImage.objects.get(id=image_id) # Pobieramy rekord obrazka z bazy po ID.
    img = Image.open(obj.image.path) # Otwieramy fizyczny plik z dysku (ścieżka z ImageField).
    width, height = img.size # Pobieramy szerokość i wysokość obrazka.

    # prosta "klasyfikacja"
    is_grayscale = img.mode in ("L", "LA") # Sprawdzamy tryb obrazu: L/LA oznacza skalę szarości.
    result = "grayscale" if is_grayscale else "color" # Tworzymy część wyniku: „grayscale” albo „color”.
    result = f"{result}, {width}x{height}" # Doklejamy wymiary do wyniku, np. color, 800x600.

    obj.classification_result = result
    obj.save(update_fields=["classification_result"]) # Zapisujemy wynik do bazy tylko w polu classification_result.
    return result

# (29) Zadanie 17
@shared_task
def generate_random_number():
    """
    Rejestruje funkcję jako zadanie Celery
    Zwraca losową liczbę całkowitą od 1 do 100
    """
    return random.randint(1, 100)

# (29) Zadanie 17
@shared_task
def multiply_by_10(value):
    """
    Zadanie Celery, które przyjmuje wartość z poprzedniego zadania.
    Mnoży wartość przez 10 i zwraca wynik.
    """
    return value * 10

# (29) Zadanie 17
@shared_task
def save_result_to_file(value):
    """
    Zadanie Celery, które przyjmuje wynik i zapisuje do pliku.
    """
    file_path = os.path.join(settings.BASE_DIR, "chain_result.txt") # Tworzy pełną ścieżkę do pliku w katalogu głównym projektu.
    with open(file_path, "a", encoding="utf-8") as f: # Otwiera plik w trybie dopisywania (a), tworzy jeśli nie istnieje.
        f.write(f"Wynik obliczeń łańcucha: {value}\n") # Dopisuje wynik i znak nowej linii.
    return value

# (29) Zadanie 20
@shared_task
def process_logentry(log_id):
    """Rejestruje funkcję jako zadanie Celery; przyjmuje ID wpisu."""
    entry = LogEntry.objects.get(id=log_id) # Pobiera rekord z bazy po ID.
    # tu dowolna logika przetwarzania
    entry.message = entry.message + " [processed]" # Modyfikuje treść wpisu, dodając dopisek.
    entry.save(update_fields=["message"]) # Zapisuje tylko zmienione pole message.
    return f"ID: {log_id}"
