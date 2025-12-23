from django.shortcuts import render
from rest_framework import viewsets
from .models import Task, Product, Note, Book, Author
from .serializers import TaskSerializer, ProductSerializer, NoteSerializer, BookSerializer, AuthorSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('-created_at') # Jakie dane mają być dostępne
    serializer_class = TaskSerializer # Jakiego serializatora użyć do "tłumaczenia"

# (25) Zadanie 3
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # (25) Zadanie 8
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

# (25) Zadanie 5
@api_view(['GET'])
def set_name_view(request):
    name = request.GET.get('name') # pobierane z query string
    response = Response({"message": "Ciasteczko zostało ustawione!"})
    # Ustawienie ciasteczka
    if name:
        response.set_cookie('user_name', name, max_age=3600)
    return response

@api_view(['GET'])
def hello_view(request):
    # Odczytanie ciasteczka 'user_name'
    user_name = request.COOKIES.get('user_name', 'Gość')
    return Response({'message': f"Witaj, {user_name}"})

# (25) Zadanie 6
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

# (25) Zadanie 7
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
    
# (25) Zadanie 9
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
