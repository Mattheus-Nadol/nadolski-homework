from fastapi import APIRouter, HTTPException, Path
from models.models import Book

router = APIRouter()

# (33) Zadanie 5 - CRUD dla książek
books_db: dict[int, Book] = {}

# (33) Zadanie 9 endpoints książek -> zamieniamy @app.get -> @router.get

# GET /books - lista wszystkich
@router.get("/books", tags=["Books"])
async def get_books():
    """
    Endpoint zwracający listę wszystkich książek.

    Wymaga nagłówka: X-API-Key

    Przykład wywołania:
    GET /books

    Przykładowa odpowiedź:
    [
        {
            "title": "Python 101",
            "author": "John Doe",
            "pages": 250
        },
        {
            "title": "FastAPI Guide",
            "author": "Jane Smith",
            "pages": 300
        }
    ]
    """
    return list(books_db.values())

# GET /books/{id} - jedna książka
@router.get("/books/{book_id}", tags=["Books"])
async def get_book(book_id: int = Path(..., description="ID książki")):
    """
    Endpoint zwracający szczegóły pojedynczej książki na podstawie ID.

    Przykład wywołania:
    GET /books/1

    Przykładowa odpowiedź:
    {
        "title": "Python 101",
        "author": "John Doe",
        "pages": 250
    }
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Nie znaleziono książki")
    return books_db[book_id]

# POST /books - dodaj książkę
@router.post("/books", status_code=201, tags=["Books"])
async def create_book(book: Book):
    """
    Endpoint do dodawania nowej książki.

    Przykład wywołania:
    POST /books
    Body:
    {
        "title": "Nowa Książka",
        "author": "Autor",
        "pages": 123
    }

    Przykładowa odpowiedź:
    {
        "title": "Nowa Książka",
        "author": "Autor",
        "pages": 123
    }
    """
    new_id = max(books_db.keys(), default=0) + 1
    books_db[new_id] = book
    return book

# DELETE /books/{id} - usuń książkę
@router.delete("/books/{book_id}", status_code=204, tags=["Books"])
async def delete_book(book_id: int = Path(..., description="ID książki")):
    """
    Endpoint do usuwania książki na podstawie ID.

    Przykład wywołania:
    DELETE /books/1

    Przykładowa odpowiedź:
    (brak treści, status 204)
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Nie znaleziono książki")
    del books_db[book_id]
    return
