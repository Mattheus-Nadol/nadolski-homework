"""
URL configuration for test_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home_view, name='home'),
    path('info/', views.info_view, name='info'),
    path('rules/', views.rules_view, name='rules'),
    path('user/<str:username>/', views.user_view, name='username'),
    path('objects/', views.objects_view, name='objects'),
    path('notes/', views.notes_view, name='notes'),
    path('notes/<int:note_id>/', views.notes_detail_view, name='notes_detail'),
    path('products/', views.product_list_view, name='product-list'),
    path('product_add/', views.product_add_view, name='product-add'),
    path('category/<int:category_id>/', views.category_view, name='category'),
]
