from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Task, Product, Note, Book, Author
from .serializers import TaskSerializer, ProductSerializer, NoteSerializer, BookSerializer, AuthorSerializer, Task7Serializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    """
    Ten widok obsługuje operacje na liście tasków.
    
    * Pozwala na pobranie listy wszystkich tasków.
    * Pozwala na dodanie nowego tasku.
    """
    queryset = Task.objects.all().order_by('-created_at') # Jakie dane mają być dostępne
    serializer_class = TaskSerializer # Jakiego serializatora użyć do "tłumaczenia"

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # (27) Zadanie 8
    @method_decorator(cache_page(600))  # Cache na 10 minut dla listy
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # (27) Zadanie 9 - własny cache dla retrieve
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        cache_key = f'product_detail_{obj.pk}'  # Prosty klucz cache z ID dla unikalności
        data = cache.get(cache_key)
        if data is None:  # Cache miss
            print(f"Cache MISS dla produktu {obj.pk}")  # Log dla testowania
            response = super().retrieve(request, *args, **kwargs)
            cache.set(cache_key, response.data, 60)  # Cache na 1 minutę
            return response
        print(f"Cache HIT dla produktu {obj.pk}")  # Log dla testowania
        return Response(data)
    
    # (27) Zadanie 9 - unieważnienie cache po update
    def perform_update(self, serializer):
        super().perform_update(serializer)
        # Unieważnij cache dla tego obiektu
        cache_key = f'product_detail_{serializer.instance.pk}'  # Ten sam klucz co w retrieve
        cache.delete(cache_key)
    
    def get_queryset(self):
        queryset = Product.objects.all()
        # request.query_params (w DRF to jest alias dla request.GET, ale oba działają).
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset

@api_view(['GET'])
def set_name_view(request):
    name = request.GET.get('name') # pobierane z query string
    response = Response({"message": "Ciasteczko zostało ustawione!"})
    # Ustawienie ciasteczka
    if name:
        response.set_cookie('user_name', name, max_age=3600)
    return response

# (27) Zadanie 3
@cache_page(60)
@api_view(['GET'])
def hello_view(request):
    # Odczytanie ciasteczka 'user_name'
    user_name = request.COOKIES.get('user_name', 'Gość')
    return Response({'message': f"Witaj, {user_name}"})

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

@api_view(['GET'])
def calculate_view(request):
    try:
        # Musimy pobrać z query string parametry:
        num1 = float(request.GET.get('num1'))
        num2 = float(request.GET.get('num2'))
        operation = request.GET.get('operation')

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return Response({'error': "Nie dzielimy przez zero"}, status=400)
            result = num1 / num2
        else:
            return Response({'error': 'Błędny operator'}, status=400)
        
        return Response({"result": result})
    
    except (TypeError, ValueError):
        return Response({"error": "Niepoprawne parametry"}, status=400)
    
class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Book.objects.all().order_by('id') # Jakie dane mają być dostępne
    serializer_class = BookSerializer # Jakiego serializatora użyć do "tłumaczenia"

class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Author.objects.all() # Jakie dane mają być dostępne
    serializer_class = AuthorSerializer # Jakiego serializatora użyć do "tłumaczenia"

@api_view(['GET'])
@permission_classes(permission_classes=[permissions.IsAuthenticated])
def protected_view(request):
    response = Response({"message": f"Zalogowany użytkownik w widoku funkcyjnym: {request.user.username}"})
    
    return response

class ProtectedView(APIView):
    permission_classes = [permissions.IsAuthenticated] # Do autentykacji
    def get(self, request):
        response = Response(
            {"message": f"Zalogowany użytkownik: {request.user.username}"},
            )
        return response
    
# W widoku można to wywołać:
from .services import get_very_complex_calculation_result

@api_view(['GET'])
def complex_view(request):
    data = get_very_complex_calculation_result()
    return Response(data)

# (27) Zadanie 7 (ulepszone podczas lekcji 28)
@api_view(['GET'])
def task_7_view(request):
    queryset = Product.objects.all()
    serializer = Task7Serializer(
        {
            "database": queryset
        }
    )

    return Response(serializer.data)

# chcemy zwrocic wiele produktow zserializowanych (stąd many=True)
# metoda list w viewsecie


# class ListModelMixin:

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#serializer ma atrybut "data" stad tez sie odwolujemy

    # def __init__(self, instance=None, data=empty, **kwargs):
    #     self.instance = instance
    #     if data is not empty:
    #         self.initial_data = data
    #     self.partial = kwargs.pop('partial', False)
    #     self._context = kwargs.pop('context', {})
    #     kwargs.pop('many', None)
    #     super().__init__(**kwargs)

