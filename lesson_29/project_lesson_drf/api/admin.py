from django.contrib import admin
from django.utils import timezone
from datetime import timedelta

from .models import Task, Note, Product, EmailNotification, LogEntry, PageTitle, UploadedImage
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

# (29) Zadanie 10
admin.site.register(EmailNotification)

# (29) Zadanie 12
@admin.action(description="Cofnij created_at o 100 dni")
def backdate_log_entries(modeladmin, request, queryset):
    new_date = timezone.now() - timedelta(days=100)
    queryset.update(created_at=new_date)

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "created_at")
    actions = [backdate_log_entries]

# (29) Zadanie 13
admin.site.register(PageTitle)

# (29) Zadanie 16
admin.site.register(UploadedImage)