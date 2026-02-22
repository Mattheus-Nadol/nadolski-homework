from fastapi import APIRouter, HTTPException, Path, Depends, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.orm_models import Book as ORMBook, Author
from models.schemas import BookCreate, BookResponse, BookUpdate

from services.background_service import send_email_log, update_statistics_after_delete

router = APIRouter()

def _fill_author_fields(book):
    """
    Pomocnicza funkcja uzupełniająca pola author_name i author_email
    na podstawie relacji ORM (selectinload).
    """
    if hasattr(book, "author") and book.author:
        book.author_name = book.author.name
        book.author_email = book.author.email

# ---------------------------------------------------------
# Async CRUD z SQLAlchemy dla książek
# ---------------------------------------------------------

from sqlalchemy.orm import selectinload

# GET /books - lista wszystkich
@router.get("/books", response_model=list[BookResponse], tags=["Books"])
async def get_books(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort_by: str | None = None
):
    """
    Endpoint zwracający listę książek z paginacją, filtrowaniem i sortowaniem.

    Query Parameters:
    - skip: offset wyników
    - limit: maksymalna liczba wyników
    - category: filtr kategorii
    - min_price: minimalna cena
    - max_price: maksymalna cena
    - sort_by:
        - price
        - title
    """

    query = select(ORMBook).options(selectinload(ORMBook.author))

    # Filtering
    if category:
        query = query.where(ORMBook.category == category)

    if min_price is not None:
        query = query.where(ORMBook.price >= min_price)

    if max_price is not None:
        query = query.where(ORMBook.price <= max_price)

    # Sorting
    if sort_by == "price":
        query = query.order_by(ORMBook.price)
    elif sort_by == "title":
        query = query.order_by(ORMBook.title)

    # Pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    books = result.scalars().all()

    for book in books:
        if book.author:
            book.author_name = book.author.name
            book.author_email = book.author.email

    return books

# GET /books/{id} - jedna książka
@router.get("/books/{book_id}", response_model=BookResponse, tags=["Books"])
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Endpoint zwracający szczegóły pojedynczej książki na podstawie ID.
    """
    result = await db.execute(select(ORMBook).options(selectinload(ORMBook.author)).where(ORMBook.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Nie znaleziono książki")
    if book.author:
        book.author_name = book.author.name
        book.author_email = book.author.email
    return book

# POST /books - dodaj książkę
@router.post("/books", response_model=BookResponse, status_code=201, tags=["Books"])
async def create_book(
    book: BookCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint do dodawania nowej książki.
    """
    result = await db.execute(select(Author).where(Author.id == book.author_id))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Nie znaleziono autora o podanym ID")
    new_book = ORMBook(
        title=book.title,
        price=book.price,
        author_id=author.id
    )
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    _fill_author_fields(new_book)

    # Background task – symulacja wysyłki email
    background_tasks.add_task(
        send_email_log,
        book_title=new_book.title,
        author_email=author.email
    )
    return new_book

# PUT /books/{id} - pełna aktualizacja książki
@router.put("/books/{book_id}", response_model=BookResponse, tags=["Books"])
async def update_book(book_id: int, updated_book: BookCreate, db: AsyncSession = Depends(get_db)):
    """
    Endpoint do pełnej aktualizacji książki (PUT).
    """
    result = await db.execute(select(ORMBook).where(ORMBook.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Nie znaleziono książki")
    result_author = await db.execute(select(Author).where(Author.id == updated_book.author_id))
    author = result_author.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Nie znaleziono autora o podanym ID")
    book.title = updated_book.title
    book.price = updated_book.price
    book.author_id = author.id
    book.author_name = author.name
    book.author_email = author.email
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book

# DELETE /books/{book_id} - usuń książkę
@router.delete("/books/{book_id}", status_code=204, tags=["Books"])
async def delete_book(
    book_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint do usuwania książki na podstawie ID.

    Jeśli książka nie istnieje -> 404
    """
    result = await db.execute(select(ORMBook).where(ORMBook.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Nie znaleziono książki")
    await db.delete(book)
    await db.commit()

    # Background task – aktualizacja statystyk
    background_tasks.add_task(
        update_statistics_after_delete
    )
    return None

# PATCH /books/{id} - częściowa aktualizacja książki
@router.patch("/books/{book_id}", response_model=BookResponse, tags=["Books"])
async def patch_book(book_id: int, book_update: BookUpdate, db: AsyncSession = Depends(get_db)):
    """
    Endpoint do częściowej aktualizacji książki (PATCH).
    """
    result = await db.execute(select(ORMBook).options(selectinload(ORMBook.author)).where(ORMBook.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Nie znaleziono książki")
    
    update_data = book_update.model_dump(exclude_unset=True)
    
    # Aktualizacja autora jeśli podano author_id
    if "author_id" in update_data:
        result_author = await db.execute(select(Author).where(Author.id == update_data["author_id"]))
        author = result_author.scalar_one_or_none()
        if not author:
            raise HTTPException(status_code=404, detail="Nie znaleziono autora o podanym ID")
        book.author_id = author.id
        update_data.pop("author_id")
    
    # Aktualizacja pozostałych pól
    for key, value in update_data.items():
        setattr(book, key, value)
    
    db.add(book)
    await db.commit()
    await db.refresh(book)

    _fill_author_fields(book)

    return book
