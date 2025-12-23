from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# (25) Zadanie 2
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name

# (25) Zadanie 6
class Note(models.Model):
    title = models.TextField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# (25) Zadanie 9
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