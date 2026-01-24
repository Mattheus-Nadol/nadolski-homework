from django.core.management.base import BaseCommand
from api.tasks import multiply
import random

# (29) Zadanie 9
# Django docs - How to create custom django-admin commands
class Command(BaseCommand):
    help = "Enqueue 50 multiply tasks with random arguments."

    def handle(self, *args, **options):
        for _ in range(50):
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            multiply.delay(a, b)
        self.stdout.write(self.style.SUCCESS("Dodano 50 zadań multiply do kolejki."))
