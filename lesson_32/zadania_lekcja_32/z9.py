"""
Prosty serwer aiohttp z bazą danych SQLAlchemy (async).
Pozwala dodawać produkty przez POST /products.

Dokumentacja:
- aiohttp: https://docs.aiohttp.org/en/stable/
- SQLAlchemy async: https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html
- asyncpg (PostgreSQL async driver): https://magicstack.github.io/asyncpg/current/
"""

import os
import asyncio
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

# Definicja bazy i modelu Product
class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    def to_dict(self):
        # Zamiana obiektu na słownik do zwrócenia jako JSON
        return {"id": self.id, "name": self.name, "price": self.price}

# Ustawienia połączenia z bazą danych PostgreSQL (async)
DATABASE_URL = os.environ.get("DB_URL", "postgresql+asyncpg://postgres:postgres@localhost/aio_test_db")
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Funkcja inicjalizująca bazę danych i tworząca tabele
async def init_db(app):
    async with engine.begin() as conn:
        # Tworzymy tabele na podstawie definicji modeli (w tym Product)
        await conn.run_sync(Base.metadata.create_all)
    # Tworzymy async_sessionmaker i zapisujemy w aplikacji
    app["db_session_factory"] = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Placeholder funkcja do czyszczenia zasobów bazy danych
async def close_db(app):
    # Tutaj można dodać kod do zamknięcia połączeń lub innych zasobów
    pass

# Handler do obsługi POST /products - dodaje nowy produkt
async def create_product(request):
    data = await request.json()
    name = data.get("name")
    price = data.get("price")

    # Walidacja danych wejściowych
    if not name or price is None:
        return web.json_response({"error": "name and price are required"}, status=400)

    # Pobieramy sesję z fabryki sesji zapisanej w aplikacji
    async_session_factory = request.app["db_session_factory"]
    async with async_session_factory() as session:
        async with session.begin():
            product = Product(name=name, price=price)
            session.add(product)
        await session.refresh(product)  # odświeżamy, aby mieć id po dodaniu

    # Zwracamy nowo utworzony produkt w formacie JSON z kodem 201
    return web.json_response(product.to_dict(), status=201)

# Funkcja tworząca i konfigurująca aplikację aiohttp
async def create_app():
    app = web.Application()
    app.router.add_post("/products", create_product)
    app.on_startup.append(init_db)  # inicjalizacja bazy przy starcie aplikacji
    app.on_cleanup.append(close_db) # czyszczenie zasobów przy zamykaniu aplikacji
    return app

# Uruchomienie serwera, jeśli skrypt jest wywołany bezpośrednio
if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)
