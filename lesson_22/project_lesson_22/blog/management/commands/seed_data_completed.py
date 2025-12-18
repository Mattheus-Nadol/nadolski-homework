import random
from django.core.management.base import BaseCommand
from faker import Faker
from blog.models import Blog, Author, Entry

class Command(BaseCommand):
    help = 'Seeds the database with sample data'
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        # Inicjalizujemy Faker
        fake = Faker('pl_PL') # Używamy polskiego wariantu
        # Stwórzmy 3 blogi
        blogs = []
        blog_names = [
            ('Blog Sportowy', 'Wszystko o sporcie'),
            ('Blog Kulinarny', 'Pyszne przepisy i recenzje'),
            ('Blog Podróżniczy', 'Relacje z podróży po świecie')
        ]
        
        for name, tagline in blog_names:
            blog = Blog.objects.create(name=name, tagline=tagline)
            blogs.append(blog)
        
        self.stdout.write(self.style.SUCCESS(f'{len(blogs)} blogs created.'))
        # Stwórzmy 10 autorów
        authors = []
        for _ in range(10):
            author = Author.objects.create(
                name=fake.name(),
                email=fake.email()
            )
            authors.append(author)
        
        self.stdout.write(self.style.SUCCESS(f'{len(authors)} authors created.'))
        # Stwórzmy 50 wpisów
        entries = []
        for _ in range(50):
            entry = Entry.objects.create(
                blog=random.choice(blogs),
                headline=fake.sentence(nb_words=6),
                body_text=fake.text(),
                pub_date=fake.date_time_this_year(),
                rating=random.randint(5, 10)
            )
            # Dodaj losowego autora
            entry.authors.add(random.choice(authors))
            entries.append(entry)
        self.stdout.write(self.style.SUCCESS(f'{len(entries)} entries created.'))
        self.stdout.write(self.style.SUCCESS('Data seeding complete.'))
