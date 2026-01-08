from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Task, Product, Note, Author, Book

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task  # Wskazujemy, który model ma być serializowany
        fields = ['id', 'title', 'description', 'completed', 'created_at'] # Wybieramy pola do "tłumaczenia"
        # Można też użyć fields = '__all__' aby wybrać wszystkie pola

# (25) Zadanie 2
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = '__all__'

# (25) Zadanie 6
class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['title', 'content', 'created_at']
    # (25) Zadanie 10
    def validate_title(self, title):
        if len(title) < 5:
            raise ValidationError("Notatka musi mieć conajmniej 5 znaków")

# (25) Zadanie 9
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

    """
    Nested serializer jest tylko do odczytu w standardowej konfiguracji.
    DRF nie potrafi automatycznie utworzyć powiązanego obiektu (np. autora) 
    z danych zagnieżdżonych, chyba że mu to jawnie powiesz.
    Dlatego nadpisujemy create() i update(), aby wyjąć author_id i przypisać go do książki.
    """
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
