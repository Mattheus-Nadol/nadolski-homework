from django.db import models

# Create your models here.
# Krok 2: Definicja modelu w pliku blog/models.py
# Model to klasa Pythona, która mapuje się na tabelę w bazie danych.
# Każdy atrybut klasy to kolumna w tabeli.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.id}: {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - [{self.price}PLN]"

class Notepad(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f"#{self.id}: {self.title}"
