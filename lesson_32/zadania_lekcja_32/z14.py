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
from sqlalchemy import Integer, String, Float, select

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
# echo=True: loguje wszystkie zapytania SQL w konsoli (przydatne do debugowania)
# future=True: włącza nowy styl API SQLAlchemy 2.0
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Funkcja inicjalizująca bazę danych i tworząca tabele
async def init_db(app):
    async with engine.begin() as conn:
        # Tworzymy tabele na podstawie definicji modeli (w tym Product)
        await conn.run_sync(Base.metadata.create_all)
    # Tworzymy async_sessionmaker i przechowujemy w app
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

    session_factory = request.app["db_session_factory"]
    async with session_factory() as session:
        async with session.begin():
            product = Product(name=name, price=price)
            session.add(product)
        await session.refresh(product)  # odświeżamy, aby mieć id po dodaniu

    # Zwracamy nowo utworzony produkt w formacie JSON z kodem 201
    return web.json_response(product.to_dict(), status=201)

# Handler do obsługi GET /products - zwraca listę wszystkich produktów
async def get_products(request):
    session_factory = request.app["db_session_factory"]
    async with session_factory() as session:
        async with session.begin():
            # Pobieramy wszystkie produkty z bazy danych
            result = await session.execute(select(Product))
            products = result.scalars().all()
    # Zamieniamy listę obiektów Product na listę słowników
    products_list = [product.to_dict() for product in products]
    # Zwracamy listę produktów jako JSON
    return web.json_response(products_list)

# Handler do obsługi GET /products/{id} - zwraca produkt o podanym id
async def get_product_by_id(request):
    product_id = request.match_info.get("id")
    session_factory = request.app["db_session_factory"]
    async with session_factory() as session:
        async with session.begin():
            result = await session.execute(select(Product).where(Product.id == int(product_id)))
            product = result.scalar_one_or_none()
            if product is None:
                raise web.HTTPNotFound()
    return web.json_response(product.to_dict())

# Handler do obsługi PUT /products/{id} - aktualizuje produkt o podanym id
async def update_product(request):
    product_id = request.match_info.get("id")
    data = await request.json()

    session_factory = request.app["db_session_factory"]
    async with session_factory() as session:
        async with session.begin():
            # Pobieramy produkt po id z bazy danych
            result = await session.execute(select(Product).where(Product.id == int(product_id)))
            product = result.scalar_one_or_none()
            if product is None:
                # Jeśli produkt nie istnieje, zwracamy 404
                raise web.HTTPNotFound()

            # Aktualizujemy pola produktu, jeśli są podane w JSON
            name = data.get("name")
            price = data.get("price")
            if name is not None:
                product.name = name
            if price is not None:
                product.price = price
            # Zmiany zostaną zapisane po wyjściu z async with session.begin()

        # Odświeżamy produkt, aby mieć aktualne dane
        await session.refresh(product)

    # Zwracamy zaktualizowany produkt jako JSON
    return web.json_response(product.to_dict())

# Funkcja tworząca i konfigurująca aplikację aiohttp
async def create_app():
    app = web.Application()
    app.router.add_post("/products", create_product)
    app.router.add_get("/products", get_products)  # Rejestracja GET /products
    app.router.add_get("/products/{id}", get_product_by_id)  # Rejestracja GET /products/{id}
    app.router.add_put("/products/{id}", update_product)  # Rejestracja PUT /products/{id}
    app.on_startup.append(init_db)  # inicjalizacja bazy przy starcie aplikacji
    app.on_cleanup.append(close_db) # czyszczenie zasobów przy zamykaniu aplikacji
    return app

# Uruchomienie serwera, jeśli skrypt jest wywołany bezpośrednio
if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)
