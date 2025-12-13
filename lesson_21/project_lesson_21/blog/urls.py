from django.urls import path
from blog import views

urlpatterns = [
    path('', views.entry_list_view, name='entry-list'),
    path('<int:blog_id>/', views.blog_detail_view, name='blog-detail'),
    path('author/<int:author_id>/', views.author_entries_view, name='author-entries'),
    path('author/', views.author_list_view, name='authors'),
    path('top_authors/', views.top_author_view, name='top-authors'),
    path('statistics/', views.blog_statistics_view, name='blog_statistics'),
]
