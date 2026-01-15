from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Task, Product, Note, Author, Book
from .services import get_complex_query

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task  # Wskazujemy, który model ma być serializowany
        fields = ['id', 'title', 'description', 'completed', 'created_at'] # Wybieramy pola do "tłumaczenia"
        # Można też użyć fields = '__all__' aby wybrać wszystkie pola

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['title', 'content', 'created_at']
    def validate_title(self, title):
        if len(title) < 5:
            raise ValidationError("Notatka musi mieć conajmniej 5 znaków")
        return title

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only=True) # Nested serializer do odczytu
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        write_only=True
        )

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_id']


    # Nested serializer jest tylko do odczytu w standardowej konfiguracji.
    # DRF nie potrafi automatycznie utworzyć powiązanego obiektu (np. autora) 
    # z danych zagnieżdżonych, chyba że mu to jawnie powiesz.
    # Dlatego nadpisujemy create() i update(), aby wyjąć author_id i przypisać go do książki.

    def create(self, validated_data):
        # Pobierz ID autora i przypisz do książki
        author = validated_data.pop('author_id')
        book = Book.objects.create(author=author, **validated_data)
        return book

    def update(self, instance, validated_data):        
        # Obsługa aktualizacji autora        
        author = validated_data.pop('author_id', None)
        if author:
            instance.author = author
            instance.title = validated_data.get('title', instance.title)
            instance.publication_year = validated_data.get(
                'publication_year', 
                instance.publication_year
                )
            instance.save()
        return instance

# Serializer odpowiedzi - (27) Zadanie 7 (ulepszone podczas lekcji 28)
class Task7Serializer(serializers.Serializer):

    data = serializers.SerializerMethodField()
    database = ProductSerializer(many=True)

    def get_data(self, obj):
        return get_complex_query()