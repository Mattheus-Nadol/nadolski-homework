from django.contrib import admin
from .models import Task, Note, Product
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass