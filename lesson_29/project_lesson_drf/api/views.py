from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from django.shortcuts import render
from django.db import transaction
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.conf import settings

from celery import chain
from celery.result import AsyncResult

from .models import Task, Product, Note, Book, Author, UploadedImage, LogEntry
from .serializers import TaskSerializer, ProductSerializer, NoteSerializer, BookSerializer, AuthorSerializer, Task7Serializer, UploadedImageSerializer
from .tasks import simulate_cpu_bound_task, hello_world_task, multiply, log_timestamp, count_users, update_user_last_login, process_video
from .tasks import send_welcome_email, long_running_task, generate_users_csv, retry_failing_request, classify_image
from .tasks import generate_random_number, multiply_by_10, save_result_to_file, process_logentry

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
    
    @method_decorator(cache_page(600))  # Cache na 10 minut dla listy
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
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

# (29) Zadanie / Konfiguracja Celery workera:

@api_view(['GET'])
def generate_report_api_view(request):
   # Wywołujemy zadanie w tle.
   # .delay() to skrót do .apply_async().
   # Aplikacja nie czeka na zakończenie zadania.
   task = simulate_cpu_bound_task.delay(20) # symulacja 20-sekundowego zadania
   # Zwracamy natychmiastową odpowiedź do użytkownika.
   # task.id to unikalny identyfikator zadania, który możemy zapisać
   # i użyć później do sprawdzenia statusu.
   return Response({
       "message": "Twoje żądanie generowania raportu zostało przyjęte i jest przetwarzane w tle.",
       "task_id": task.id
   })

# (29) Zadanie 1
@api_view(['GET'])
def hello_celery(request):
    task = hello_world_task.delay()
    return Response({
       "message": "Właśnie przywitałeś się z Celery",
       "task_id": task.id
   })

# (29) Zadanie 2
# aby móc w ładny sposób wpisywać w Swagger, rozbudowujemy:
@extend_schema(
    request=OpenApiTypes.OBJECT,
    examples=[
        OpenApiExample(
            'Multiply Example',
            value={'a': 3.5, 'b': 2.0},
            request_only=True,
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    summary="Multiply two numbers asynchronously",
    description="Submits a multiplication task to Celery and returns the task ID.",
)
@api_view(['POST'])
def multiply_view(request):
    a = request.data.get('a')
    b = request.data.get('b')
    if a is None or b is None:
        return Response({'error': 'Provide a and b'}, status=400)
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return Response({'error': 'a and b must be numbers'}, status=400)
    task = multiply.delay(a, b)
    return Response({'task_id': task.id, 'message': 'Task submitted'})

# (29) Zadanie 3
@api_view(['GET'])
def log_timestamp_view(request):
    task = log_timestamp.delay()
    return Response({
        "message": "Timestamp zapisany do log.txt w tle",
        "task_id": task.id
    })

# (29) Zadanie 5
@api_view(['GET'])
def count_users_view(request):
    task = count_users.delay()
    return Response({
        "message": "Zadanie count_users uruchomione",
        "task_id": task.id
    })

# (29) Zadanie 7
@api_view(['GET'])
def update_user_last_login_view(request, user_id):
    task = update_user_last_login.delay(user_id)
    return Response({
        "message": "Zadanie update_user_last_login uruchomione",
        "task_id": task.id
    })

# (29) Zadanie 8
@api_view(['GET'])
def process_video_view(request):
    task = process_video.delay()
    return Response({
        "message": "Przetwarzanie wideo rozpoczęte!",
        "task_id": task.id
    })

# (29) Zadanie 10
@api_view(['GET'])
def send_email_notification_view(request, notification_id):
    task = send_welcome_email.delay(notification_id)
    return Response({
        "message": "Wysyłka maila rozpoczęta",
        "task_id": task.id
    })

# (29) Zadanie 11
@api_view(['GET'])
def start_long_task_view(request):
    task = long_running_task.delay()
    return Response({"task_id": task.id})

# (29) Zadanie 11
@api_view(['GET'])
def task_status_view(request, task_id):
    result = AsyncResult(task_id)
    response = {
        "task_id": task_id,
        "state": result.state,
    }
    if result.state == "PROGRESS":
        response.update(result.info or {})
    elif result.state == "SUCCESS":
        response.update(result.result or {})
    return Response(response)

# (29) Zadanie 14
@api_view(['GET'])
def generate_users_csv_view(request):
    task = generate_users_csv.delay()
    return Response({"task_id": task.id})

# (29) Zadanie 14
@api_view(['GET'])
def users_csv_status_view(request, task_id):
    result = AsyncResult(task_id)
    data = {"task_id": task_id, "state": result.state}

    if result.state == "SUCCESS":
        file_path = result.result.get("file_path")
        data["file_url"] = settings.MEDIA_URL + file_path
    return Response(data)

# (29) Zadanie 15
@api_view(['GET'])
def retry_failing_request_view(request):
    task = retry_failing_request.delay()
    return Response({"task_id": task.id})

# (29) Zadanie 15 (aby sprawdzić status)
@api_view(['GET'])
def retry_task_status_view(request, task_id):
    result = AsyncResult(task_id)
    return Response({
        "task_id": task_id,
        "state": result.state,
        "info": str(result.info) if result.info else None,
    })

# (29) Zadanie 16
class UploadImageView(generics.CreateAPIView):
    """Gotowy widok DRF do tworzenia obiektów (POST)."""
    queryset = UploadedImage.objects.all() # Queryset potrzebny DRF do obsługi widoku
    serializer_class = UploadedImageSerializer # Mówimy DRF, jak serializować dane i jakie pola przyjmować
    parser_classes = [MultiPartParser, FormParser] # Pozwala przyjmować pliki z multipart/form-data.

    def perform_create(self, serializer):
        """Po zapisie obrazka uruchamiamy task Celery w tle, przekazując ID."""
        obj = serializer.save()
        classify_image.delay(obj.id)

# (29) Zadanie 16
@api_view(['GET'])
def image_status_view(request, image_id):
    """Prosty endpoint GET do sprawdzenia statusu danego obrazka."""
    obj = UploadedImage.objects.get(id=image_id) # Pobieramy obiekt z bazy.
    return Response({
        "id": obj.id,
        "image": obj.image.url if obj.image else None,
        "classification_result": obj.classification_result,
    }) # Zwracamy ID, URL obrazka i wynik klasyfikacji.

# (29) Zadanie 17
@api_view(['GET'])
def run_chain_view(request):
    """
    Definiuje widok HTTP GET, który uruchamia cały łańcuch.
    Buduje łańcuch trzech zadań i od razu go uruchamia:
    """
    task = chain(
        generate_random_number.s(), # .s() tworzy „podpis” zadania,
        multiply_by_10.s(),
        save_result_to_file.s(),
    )() # () na końcu wysyła cały łańcuch do Celery.
    return Response({"task_id": task.id}) # Zwraca ID pierwszego zadania w łańcuchu.

# (29) Zadanie 20
@api_view(['POST'])
def create_logentry_and_process(request):
    """Definiuje endpoint POST, który tworzy wpis i uruchamia task."""
    with transaction.atomic(): # Startuje transakcję atomową (wszystko albo nic).
        entry = LogEntry.objects.create(message="Nowy wpis") # Tworzy nowy rekord w bazie (jeszcze niezatwierdzony).
        # uruchom task dopiero po zatwierdzeniu transakcji
        transaction.on_commit(lambda: process_logentry.delay(entry.id)) # Ustawia „hak”: task wystartuje dopiero po udanym commit.
    return Response({"id": entry.id, "message": "Utworzono i zlecono przetwarzanie"}) # Zwraca odpowiedź z ID i potwierdzeniem.

# transaction.atomic() gwarantuje, że zapis jest „wszystko albo nic”.
# transaction.on_commit(...) gwarantuje, że zadanie wystartuje dopiero po tym „nic” zamieni się w „wszystko”, 
# czyli po zatwierdzeniu transakcji.
# Czyli: atomic zapewnia spójność danych, a on_commit zapewnia, że task nie wystartuje zbyt wcześnie.