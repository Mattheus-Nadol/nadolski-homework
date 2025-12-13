from django.contrib import admin

# Register your models here.
"""Rejestracja modelu w pliku blog/admin.py"""
# Dzięki temu model 'Post' pojawi się w panelu administratora.

from .models import Entry, Blog, Author  # Importujemy nasz model

admin.site.register(Entry) # Rejestrujemy model
admin.site.register(Blog)
admin.site.register(Author)