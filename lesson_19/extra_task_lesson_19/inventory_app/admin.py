from django.contrib import admin

# Register your models here.
from .models import Product, Customer, Order


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
