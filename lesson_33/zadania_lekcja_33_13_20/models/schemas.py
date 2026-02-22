from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

# ------------------------------
# Book Schemas
# ------------------------------
class BookCreate(BaseModel):
    """
    Schema do tworzenia książki. 
    Zamiast podawać imię i email autora, wystarczy podać author_id.
    Zapobiega to pomyłkom przy wpisywaniu danych autora.
    """
    title: str
    price: float
    author_id: int  # teraz identyfikujemy autora po ID

    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    """
    Schema do częściowej aktualizacji książki (PATCH).
    Wszystkie pola są opcjonalne, ponieważ można aktualizować tylko wybrane atrybuty książki.
    Zamiast podawać imię i email autora, można podać author_id.
    """
    title: Optional[str] = None
    price: Optional[float] = None
    author_id: Optional[int] = None  # aktualizacja autora przez ID

    model_config = ConfigDict(from_attributes=True)


class BookResponse(BaseModel):
    """
    Schema do zwracania książki z API.
    Zawiera wszystkie dane, w tym imię i email autora.
    """
    id: int
    title: str
    price: float
    author_name: Optional[str] = None
    author_email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ------------------------------
# Author Schemas
# ------------------------------
class AuthorCreate(BaseModel):
    """
    Schema do tworzenia autora.
    Zawiera podstawowe informacje: imię i email.
    """
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class AuthorResponse(BaseModel):
    """
    Schema do zwracania autora z API.
    Zawiera dane autora oraz listę jego książek.
    """
    id: int
    name: str
    email: EmailStr
    books: Optional[List[BookResponse]] = []

    model_config = ConfigDict(from_attributes=True)


# ------------------------------
# Blog API Schemas
# ------------------------------

class UserCreate(BaseModel):
    """
    Schema do tworzenia użytkownika bloga.
    """
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    """
    Schema odpowiedzi dla użytkownika bloga.
    """
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class PostCreate(BaseModel):
    """
    Schema do tworzenia posta blogowego.
    Tylko autor może tworzyć posty.
    """
    title: str
    content: str
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class PostUpdate(BaseModel):
    """
    Schema do częściowej aktualizacji posta.
    Tylko autor posta może go edytować.
    """
    title: Optional[str] = None
    content: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PostResponse(BaseModel):
    """
    Schema odpowiedzi posta blogowego.
    Zawiera autora oraz komentarze.
    """
    id: int
    title: str
    content: str
    author_id: int
    author: Optional[UserResponse] = None
    comments: Optional[List["CommentResponse"]] = []

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    """
    Schema do tworzenia komentarza do posta.
    """
    content: str
    post_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(BaseModel):
    """
    Schema odpowiedzi komentarza.
    """
    id: int
    content: str
    post_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# Resolve forward references
PostResponse.model_rebuild()


"""
Różnica między ORM modelem a Pydantic schema:
- ORM model reprezentuje strukturę bazy danych i jest używany do interakcji z bazą (np. SQLAlchemy).
- Pydantic schema służy do walidacji, serializacji i deserializacji danych w API.

Dlaczego używamy schema do API:
- Zapewniają walidację danych wejściowych i kontrolę nad danymi wyjściowymi.
- Ułatwiają konwersję między ORM a formatem JSON.
- Zwiększają bezpieczeństwo i czytelność kodu.

Dokumentacja:
- Pydantic: https://pydantic.dev/
- FastAPI: https://fastapi.tiangolo.com/
"""
