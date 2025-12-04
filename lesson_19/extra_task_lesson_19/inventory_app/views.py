from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.urls import reverse


def home(request):
    admin_url = reverse('admin:index')
    html = f"""
    <h1>Hello! Welcome to Inventory!</h1>
    <p><a href="{admin_url}">Go to Admin</a></p>
    """
    return HttpResponse(html)

