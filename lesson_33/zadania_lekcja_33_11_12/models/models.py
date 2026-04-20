# (33) Zadanie 4 - model
from pydantic import BaseModel, Field, EmailStr, field_validator  # pip install email-validator


class Product(BaseModel):
    """
    Model produktu z walidacją własną (custom validators).

    Pola:
    - name: tylko litery i cyfry
    - price: musi być > 0 oraz <= 10000
    - quantity: liczba nieujemna
    - category: jedna z dozwolonych wartości

    Custom validators pozwalają na tworzenie własnych reguł walidacji,
    gdy standardowe ograniczenia Field() nie są wystarczające.

    Dokumentacja:
    https://docs.pydantic.dev/latest/concepts/validators/
    """

    name: str = Field(..., description="Nazwa produktu (tylko litery i cyfry)")
    price: float = Field(..., description="Cena produktu (>0 i <=10000)")
    quantity: int = Field(..., ge=0, description="Ilość produktu (nieujemna)")
    category: str = Field(..., description="Kategoria produktu")

    # Lista dozwolonych kategorii – stała klasowa
    ALLOWED_CATEGORIES = ["Electronics", "Books", "Clothing"]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """
        Sprawdza czy nazwa zawiera wyłącznie litery i cyfry.

        isalnum() zwraca True tylko wtedy, gdy string
        składa się wyłącznie z liter i cyfr.
        """
        if not value.isalnum():
            raise ValueError("Nazwa produktu może zawierać tylko litery i cyfry.")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        """
        Sprawdza czy cena jest w zakresie (0, 10000].

        Jeśli warunek nie jest spełniony,
        Pydantic zgłosi błąd walidacji (422 w FastAPI).
        """
        if value <= 0 or value > 10000:
            raise ValueError("Cena musi być większa niż 0 i mniejsza lub równa 10000.")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        """
        Sprawdza czy kategoria znajduje się na liście dozwolonych wartości.

        Dzięki temu ograniczamy dane wejściowe do kontrolowanego zbioru.
        """
        if value not in cls.ALLOWED_CATEGORIES:
            raise ValueError(
                f"Kategoria musi być jedną z: {cls.ALLOWED_CATEGORIES}"
            )
        return value

# (33) Zadanie 11 - nested models with detailed comments and docstrings

class Author(BaseModel):
    """
    Model reprezentujący autora książki.

    Pola:
    - name: Imię i nazwisko autora (str)
    - email: Adres email autora (EmailStr)

    Używamy EmailStr, aby zapewnić, że podany adres email jest poprawny
    zgodnie z definicją RFC. EmailStr to specjalny typ Pydantic, który
    automatycznie waliduje poprawność adresów email.

    Dokumentacja EmailStr:
    https://docs.pydantic.dev/latest/concepts/types/#emailstr
    """
    name: str
    email: EmailStr

class Book(BaseModel):
    """
    Model książki zagnieżdżony z modelem autora.

    Pola:
    - title: Tytuł książki (str)
    - author: Obiekt Author (zagnieżdżony model)
    - price: Cena książki (float)

    Zagnieżdżone modele (nested models) pozwalają na strukturalne
    grupowanie danych w modelach Pydantic. Dzięki temu możemy
    tworzyć bardziej złożone i czytelne schematy danych.

    Pydantic automatycznie waliduje dane zagnieżdżone, wywołując
    walidację na modelu wewnętrznym (np. Author w Book). Jeśli
    dane autora są niepoprawne, cała walidacja modelu Book również
    się nie powiedzie.

    Dokumentacja nested models:
    https://docs.pydantic.dev/latest/concepts/models/
    """
    title: str
    author: Author
    price: float

# (33) Zadanie 7 - model
class User(BaseModel):
    email: EmailStr