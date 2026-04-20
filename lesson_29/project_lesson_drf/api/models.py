from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.TextField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Author(models.Model):
    name = models.TextField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.TextField(max_length=100)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return self.title
    
# (29) Zadanie 10
class EmailNotification(models.Model):
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.recipient_email} | {self.subject}"

# (29) Zadanie 12
class LogEntry(models.Model):
    # krótka wiadomość do logu
    message = models.CharField(max_length=255)
    # automatyczny czas utworzenia wpisu
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M:%S} | {self.message}"

# (29) Zadanie 13
class PageTitle(models.Model):
    """
    Przechowuje tytuł strony pobrany przez zadanie Celery.
    Model jest potrzebny, bo w treści zadania jest zapis do bazy danych.
    """
    url = models.URLField()
    title = models.CharField(max_length=255)
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} | {self.url}"

# (29) Zadanie 16
class UploadedImage(models.Model):
    image = models.ImageField(upload_to="uploads/")
    classification_result = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"UploadedImage {self.id}"
