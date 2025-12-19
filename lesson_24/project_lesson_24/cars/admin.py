from django.contrib import admin
from django.utils.html import format_html
from .models import Car, Dealer
# Register your models here.

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):

    list_display = ("brand", "model", "year", "is_available", "full_name", "display_photo")
    search_fields = ("brand", "model")
    list_filter = ("is_available", "year")
    ordering = ["-year"]
    readonly_fields = ["year"]
    actions = ["mark_as_unavailable"]

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="150">', obj.photo.url)
        return "Brak zdjęcia"
    display_photo.short_description = "Zdjęcie"

    @admin.display(description="Pełna nazwa")
    def full_name(self, obj):
        return f"{obj.brand} {obj.model}"
    
    @admin.display(description="Oznacz jako niedostępne")
    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    # mark_as_unavailable.short_description = "Oznacz jako niedostępne" (alternatywnie)

class CarInLine(admin.TabularInline):
    # Model do wyświetlania
    model = Car
    # Ile extra pól do uzupełnienia
    extra = 1

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ["name"]
    # dołączamy inline do widoku admina Dealera
    inlines = [CarInLine]

