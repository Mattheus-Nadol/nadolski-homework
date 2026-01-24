# project_name/celery.py

import os
from celery import Celery

# Ustawienie domyślnej zmiennej środowiskowej dla Django
# Dzięki temu Celery będzie wiedziało, gdzie znaleźć ustawienia projektu.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lesson_drf.settings')

# Utworzenie instancji aplikacji Celery
app = Celery('lesson_drf')

# Wczytanie konfiguracji z pliku settings.py Django.
# Używamy namespace='CELERY', aby wszystkie ustawienia Celery
# w settings.py musiały zaczynać się od prefiksu CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatyczne wykrywanie i rejestrowanie zadań z plików tasks.py
# we wszystkich aplikacjach Django zainstalowanych w projekcie.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')