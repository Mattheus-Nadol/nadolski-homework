from django.urls import path
from blog import views

urlpatterns = [
    path('', views.EntryListView.as_view(), name='entry-list'),
    path('<int:blog_id>/entries/', views.blog_detail_view, name='blog-detail'),
    path('author/<int:author_id>/', views.author_entries_view, name='author-entries'),
    path('author/', views.author_list_view, name='authors'),
    path('top_authors/', views.top_author_view, name='top-authors'),
    path('stats/', views.StatListView.as_view(), name='stats'),
    path('contact/', views.contact_view, name='contact'),
    path('register/', views.register, name='register'),
]
