from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Car, Dealer
from django.db.models import Avg, Count, Q

class CarListView(ListView):
    """Widok wyświetlający wszystkie samochody"""
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'
    paginate_by = 10
    ordering = ['-year']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrowanie po dostępności
        available = self.request.GET.get('available')
        if available == 'true':
            queryset = queryset.filter(is_available=True)
        elif available == 'false':
            queryset = queryset.filter(is_available=False)
        
        # Wyszukiwanie po marce lub modelu
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(brand__icontains=search) | Q(model__icontains=search)
            )
        
        return queryset

def car_detail_view(request, car_id):
    """Widok szczegółów samochodu"""
    car = get_object_or_404(Car, id=car_id)
    context = {
        'car': car,
    }
    return render(request, 'cars/car_detail.html', context)

def dealer_list_view(request):
    """Lista wszystkich dealerów"""
    dealers = Dealer.objects.annotate(car_count=Count('car')).order_by('-car_count')
    context = {
        'dealers': dealers,
    }
    return render(request, 'cars/dealer_list.html', context)

def dealer_detail_view(request, dealer_id):
    """Widok samochodów konkretnego dealera"""
    dealer = get_object_or_404(Dealer, id=dealer_id)
    cars = Car.objects.filter(dealer=dealer).order_by('-year')
    avg_price = cars.aggregate(avg_price=Avg('price'))['avg_price']
    
    context = {
        'dealer': dealer,
        'cars': cars,
        'avg_price': avg_price,
        'car_count': cars.count(),
    }
    return render(request, 'cars/dealer_detail.html', context)

def car_statistics_view(request):
    """Statystyki samochodów"""
    total_cars = Car.objects.count()
    available_cars = Car.objects.filter(is_available=True).count()
    unavailable_cars = Car.objects.filter(is_available=False).count()
    
    avg_price = Car.objects.aggregate(avg_price=Avg('price'))['avg_price']
    avg_year = Car.objects.aggregate(avg_year=Avg('year'))['avg_year']
    
    # Najdroższe samochody
    most_expensive = Car.objects.order_by('-price')[:5]
    
    # Najnowsze samochody
    newest_cars = Car.objects.order_by('-year')[:5]
    
    # Statystyki po marce
    brand_stats = Car.objects.values('brand').annotate(
        count=Count('id'),
        avg_price=Avg('price')
    ).order_by('-count')
    
    context = {
        'total_cars': total_cars,
        'available_cars': available_cars,
        'unavailable_cars': unavailable_cars,
        'avg_price': avg_price,
        'avg_year': avg_year,
        'most_expensive': most_expensive,
        'newest_cars': newest_cars,
        'brand_stats': brand_stats,
    }
    return render(request, 'cars/car_statistics.html', context)
