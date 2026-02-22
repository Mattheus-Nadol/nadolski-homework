from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models.orm_models import Author
from models.schemas import AuthorCreate, AuthorResponse, BookResponse

router = APIRouter()

# ------------------------
# POST /authors - dodaj autora
# ------------------------
@router.post("/authors", response_model=AuthorResponse, status_code=201, tags=["Authors"])
async def create_author(author: AuthorCreate, db: AsyncSession = Depends(get_db)):
    """
    Endpoint do tworzenia nowego autora w bazie.

    FastAPI + Pydantic:
    - waliduje dane wejściowe za pomocą AuthorCreate
    - automatycznie serializuje wynik do AuthorResponse

    Przykład wywołania:
    POST /authors
    Body:
    {
        "name": "Jan Kowalski",
        "email": "jan@example.com"
    }

    Przykładowa odpowiedź:
    {
        "id": 1,
        "name": "Jan Kowalski",
        "email": "jan@example.com",
        "books": []
    }

    Dokumentacja:
    - https://fastapi.tiangolo.com/tutorial/body/
    - https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    """
    new_author = Author(
        name=author.name,
        email=author.email
    )
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    # Zwracamy AuthorResponse z pustą listą książek, aby uniknąć błędów związanych z asynchronicznymi relacjami
    return AuthorResponse(
        id=new_author.id,
        name=new_author.name,
        email=new_author.email,
        books=[]
    )

# ------------------------
# GET /authors/{id}/books - książki autora
# ------------------------
@router.get("/authors/{author_id}/books", response_model=AuthorResponse, tags=["Authors"])
async def get_author_books(author_id: int = Path(..., description="ID autora"), db: AsyncSession = Depends(get_db)):
    """
    Endpoint zwracający autora wraz z jego książkami.

    Relacja 1:N (Author -> Books) jest ładowana używając selectinload() dla eager loading.
    
    Przykład wywołania:
    GET /authors/1/books

    Przykładowa odpowiedź:
    {
        "id": 1,
        "name": "Jan Kowalski",
        "email": "jan@example.com",
        "books": [
            {
                "id": 1,
                "title": "FastAPI Mastery",
                "price": 99.99,
                "author_name": "Jan Kowalski",
                "author_email": "jan@example.com"
            }
        ]
    }

    Dokumentacja:
    - https://docs.sqlalchemy.org/en/20/orm/loading_relationships.html#eager-loading
    """
    result = await db.execute(
        select(Author).options(selectinload(Author.books)).where(Author.id == author_id)
    )
    author = result.scalars().first()
    if not author:
        raise HTTPException(status_code=404, detail="Nie znaleziono autora")

    # Uzupełnienie author_name i author_email dla książek
    for book in author.books:
        book.author_name = author.name
        book.author_email = author.email

    return author

# ------------------------
# GET /authors - wszyscy autorzy
# ------------------------
@router.get("/authors/", response_model=list[AuthorResponse], tags=["Authors"])
async def get_all_authors(db: AsyncSession = Depends(get_db)):
    """
    Endpoint zwracający listę wszystkich autorów w bazie wraz z ich książkami.
    """
    result = await db.execute(
        select(Author).options(selectinload(Author.books))
    )
    authors = result.scalars().all()
    # Konwertujemy ORM na AuthorResponse, aby uniknąć problemów z asynchronicznymi relacjami
    response = []
    for author in authors:
        response.append(
            AuthorResponse(
                id=author.id,
                name=author.name,
                email=author.email,
                books=[
                    BookResponse(
                        id=book.id,
                        title=book.title,
                        price=book.price,
                        author_name=author.name,
                        author_email=author.email
                    ) for book in author.books
                ]
            )
        )
    return response