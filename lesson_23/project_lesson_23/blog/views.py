from datetime import date, timedelta
from django.utils import timezone

from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg
from .models import Entry, Blog, Author
from .forms import CommentSearch, ContactForm
from django.contrib import messages
from django.db.models.functions import TruncMonth

def home_view(request):
    """Widok strony głównej z nawigacją do ADMIN i BLOG"""
    return render(request, 'index.html')

#Zadanie 9 - przerobiony widok funkcyjny na klasowy (entry_list_view)
class EntryListView(ListView):
    """Widok wyświetlający wszystkie wpisy blogowe 
    z opcją wyszukiwania po minimalnej ilości komentarzy."""
    model = Entry
    template_name = 'blog/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 5
    ordering = ['-number_of_comments']

    def get_queryset(self):
        """Nadpisanie QuerySet - działa jak Entry.objects.all() ale z 
        customizacją"""
        queryset = super().get_queryset()

        # Tworzymy instancję formularza na podstawie danych GET
        form = CommentSearch(self.request.GET or None)
        if form.is_valid():
            min_comments = form.cleaned_data.get('min_comments')
            if min_comments is not None:
                queryset = queryset.filter(number_of_comments__gte=min_comments)
        
        # Posty z ostatnich 7 dni
        recent = self.request.GET.get('recent')
        if recent == 'true':
            week_ago = timezone.now() - timedelta(days=7)
            queryset = queryset.filter(pub_date__gte=week_ago)
        return queryset

    def get_context_data(self, **kwargs):
        """Dodanie formularza do kontekstu"""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentSearch(self.request.GET or None)
        return context

def blog_detail_view(request, blog_id):
    """Widok szczegółów bloga z jego wpisami"""
    blog = get_object_or_404(Blog, id=blog_id)
    blog_entries = Entry.objects.filter(blog=blog).prefetch_related('authors').order_by('-pub_date')
    total_comments = Entry.objects.filter(blog=blog).aggregate(total_comments=Sum('number_of_comments'))['total_comments']
    context = {
        'blog': blog,
        'entries': blog_entries,
        'total_comments': total_comments,
    }
    return render(request, 'blog/blog_detail.html', context)

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

def contact_view(request):
    """Formularz kontatkowy z użyciem crispy-forms"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # In a real app you'd send an email or persist the message.
            messages.success(request, 'Dziękujemy — wiadomość została wysłana.')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'blog/contact_form.html', {'form': form})

# Zadanie 10
class StatListView(TemplateView):
    """Statystyki z:
    - liczbą wpisów dla każdego bloga
    - średnią oceną wpisów każdego autora
    - 5 najlepiej ocenianych wpisów
    - wykres tekstowy z wpisami opublikowanymi w każdym miesiącu
    (użyj metod aggregate() i annotate())
    """
    template_name = 'blog/blog_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.annotate(entry_count=Count('entry'))
        avg_authors = Author.objects.annotate(avg_rating=Avg('entry__rating'))
        top_entries = Entry.objects.order_by('-rating')[:5]
        monthly_entries = Entry.objects.annotate(month=TruncMonth('pub_date')).values('month').annotate(count=Count('id')).order_by('month')
        
        # Calculate max count for monthly chart scaling
        max_monthly_count = max([m['count'] for m in monthly_entries], default=1)
        
        context = {
            'blogs': blogs,
            'avg_authors': avg_authors,
            'top_entries': top_entries,
            'monthly_entries': monthly_entries,
            'max_monthly_count': max_monthly_count
        }
        return context

