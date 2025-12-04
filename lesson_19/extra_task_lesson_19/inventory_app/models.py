from django.db import models

# Create your models here.

import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    available_since = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    barcode = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.name


class Customer(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    registered_at = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(blank=True, null=True)
    is_vip = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'), # (wartość w bazie danych, etykieta dla użytkownika)
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_express = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.order_number} - {self.status}"
