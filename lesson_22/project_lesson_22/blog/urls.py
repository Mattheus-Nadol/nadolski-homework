from django.urls import path
from blog import views

urlpatterns = [
    path('', views.EntryListView.as_view(), name='entry-list'),
    path('<int:blog_id>/entries/', views.blog_detail_view, name='blog-detail'),
    path('contact/', views.contact_view, name='contact'),
    path('stats/', views.StatListView.as_view(), name='stats'),
]