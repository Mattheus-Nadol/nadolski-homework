from django.contrib import admin

# Register your models here.
from .models import Entry, Blog, Author, Category  # Importujemy nasz model

admin.site.register(Entry) # Rejestrujemy model
admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Category)