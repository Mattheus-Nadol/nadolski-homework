from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from blog.models import Post, Notepad, Product, Category
from blog.forms import ProductForm

# Create your views here.
def home_view(request):
    return HttpResponse("<h1>Strona Startowa</h1>")

def info_view(request):
    """Informacje o stronie"""
    return HttpResponse("<h2>Informacje o stronie</h2>")

def rules_view(request):
    """Regulamin"""
    return HttpResponse("<h2>Regulamin</h2>")

def user_view(request, username):
    return HttpResponse(f"<h2>Witaj na profilu: {username.title()}!</h2>")

def objects_view(request):
    all_posts = Post.objects.all().order_by('id')
    return render(request, 'objects.html', {'all_posts':all_posts}) # context musi być słownikiem

def notes_view(request):
    all_notes = Notepad.objects.all().order_by('id')
    paginator = Paginator(all_notes, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'notes_general.html', context)

def notes_detail_view(request, note_id):
    all_notes = Notepad.objects.get(id=note_id)
    return render(request, 'notes_detail.html', {'all_notes': all_notes})

def product_list_view(request):
    all_products = Product.objects.all().order_by('id')
    context ={
        'all_products': all_products
    }
    return render(request, 'product_list.html', context)

def product_add_view(request):
    if request.method == 'POST':
        # Jeśli formularz został wysłany, tworzymy instancję z danymi POST
        form = ProductForm(request.POST)
        if form.is_valid():
            # Jeśli dane są poprawne, możemy je przetworzyć
            # Pobierz wartość z pola 'search'
            product_name = form.cleaned_data['name']
            product_description = form.cleaned_data['description']
            product_price = form.cleaned_data['price']
            Product.objects.create(name=product_name, description=product_description, price=product_price)
            # Przekierowujemy użytkownika, aby uniknąć ponownego wysłania formularza
            return redirect('/products')
    else:
        # Jeśli to zapytanie GET, tworzymy pusty formularz
        form = ProductForm()
    return render(request, 'product_add.html', {'form': form}) # form jako 'context'

def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    categorized_products = Product.objects.filter(category_id=category_id)
    context = {
        'categorized_products' : categorized_products,
        'category': category,
    }
    return render(request, 'category_details.html', context)