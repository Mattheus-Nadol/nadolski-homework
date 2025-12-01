from django.contrib import admin

# Register your models here.
from .models import Ogloszenie  # Importujemy nasz model

class Details(admin.ModelAdmin):
    list_display = ["title", "price", "date_add", "date_update"]
    
admin.site.register(Ogloszenie, Details) # Rejestrujemy model


