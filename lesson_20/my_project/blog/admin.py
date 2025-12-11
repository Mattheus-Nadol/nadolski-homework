from django.contrib import admin

# Register your models here.
# Krok 3: Rejestracja modelu w pliku blog/admin.py
# Dzięki temu model 'Post' pojawi się w panelu administratora.

from .models import Post, Product, Notepad, Category  # Importujemy nasz model

admin.site.register(Post) # Rejestrujemy model
admin.site.register(Product)
admin.site.register(Notepad)
admin.site.register(Category)