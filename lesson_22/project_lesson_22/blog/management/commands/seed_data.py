import random
from django.core.management.base import BaseCommand
from faker import Faker
from blog.models import Blog, Author, Entry, Category

class Command(BaseCommand):
    help = 'Seeds the database with sample data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Inicjalizujemy Faker
        fake = Faker('pl_PL') # Używamy polskiego wariantu
        
        # Stwórzmy 6 kategorii
        categories = []
        for _ in range(6):
            category = Category.objects.create(
                name=fake.domain_word().capitalize()
            )
            categories.append(category)
        
        self.stdout.write(self.style.SUCCESS(f'{len(categories)} categories created.'))

        # Pobieramy wszystkie wpisy
        entries = list(Entry.objects.all())
        # Dodaj losową kategorię
        for entry in entries:
            entry.category.add(random.choice(categories))

        self.stdout.write(self.style.SUCCESS('Data seeding complete.'))
