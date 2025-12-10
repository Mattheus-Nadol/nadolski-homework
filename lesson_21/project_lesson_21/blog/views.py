from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg
from .models import Entry, Blog, Author
from .forms import TitleSearch

def home_view(request):
    """Widok strony głównej z nawigacją do ADMIN i BLOG"""
    return render(request, 'index.html')

def entry_list_view(request):
    """Widok wyświetlający wszystkie wpisy blogowe z opcją wyszukiwania po tytule."""
    # Tworzymy instancję formularza na podstawie danych GET
    form = TitleSearch(request.GET or None)
    recent = request.GET.get('recent')
    

    # Pobieramy wszystkie wpisy z powiązanymi obiektami (optymalizacja)
    all_entries = Entry.objects.select_related('blog').prefetch_related('authors').order_by('-rating').filter(rating__gt=7)

    # Sprawdamy, czy formularz jest poprawny i czy podano frazę wyszukiwania
    if form.is_valid():
        # Pobierz wartość z pola 'search'
        search_term = form.cleaned_data['search']
        # Dodaj filtr wyszukiwania po tytule (headline__icontains)
        all_entries = all_entries.filter(headline__icontains=search_term)
    if recent == 'true':
        last_week = date.today() - timedelta(days=7)
        all_entries = all_entries.filter(pub_date__gte=last_week)

    # Tworzymy kontekst - słownik danych do przekazania do szablonu
    context = {
        'entries': all_entries,
        'form': form,
    }

    return render(request, 'blog/entry_list.html', context)

def blog_detail_view(request, blog_id):
    """Widok szczegółów bloga z jego wpisami"""
    try:
        blog = Blog.objects.get(id=blog_id)
        blog_entries = Entry.objects.filter(blog=blog).prefetch_related('authors').order_by('-pub_date')
        total_comments = Entry.objects.filter(blog=blog).aggregate(total_comments=Sum('number_of_comments'))['total_comments']

        context = {
            'blog': blog,
            'entries': blog_entries,
            'total_comments': total_comments,
        }
        return render(request, 'blog/blog_detail.html', context)
    
    except Blog.DoesNotExist:
        # W prawdziwej aplikacji użylibyśmy Http404 lub get_object_or_404
        context = {'error': 'Blog nie został znaleziony'}
        return render(request, 'blog/error.html', context)

def author_entries_view(request, author_id):
    """Widok wpisów konkretnego autora"""
    try:
        author = Author.objects.get(id=author_id)
        author_entries = Entry.objects.filter(authors=author).select_related('blog').order_by('-pub_date')
        
        context = {
            'author': author,
            'entries': author_entries,
        }
        return render(request, 'blog/author_detail.html', context)
    
    except Author.DoesNotExist:
        context = {'error': 'Autor nie został znaleziony'}
        return render(request, 'blog/error.html', context)
    
def author_list_view(request):
    """Lista wszystkich autorów wraz z adresem email"""
    # Pobieramy wszystkicj autorów (optymalizacja)
    all_authors = Author.objects.all()
    
    # Tworzymy kontekst - słownik danych do przekazania do szablonu
    context = {
        'authors': all_authors,
    }
    return render(request, 'blog/author_list.html', context)

def top_author_view(request):
    """Lista autorów posortowana po ilości wpisów"""
    top_authors = Author.objects.annotate(num_entries=Count('entry')).order_by('-num_entries')

    context = {
        'top_authors' : top_authors,
    
    }
    return render(request, 'blog/top_authors.html', context)

def blog_statistics_view(request):
    """Widok statystyk wszystkich blogów"""
    blogs = Blog.objects.annotate(entry_count=Count('entry')).annotate(avg_rating=Avg('entry__rating'))
    
    context = {
        'blogs': blogs,
    }
    return render(request, 'blog/blog_statistics.html', context)

