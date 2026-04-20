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
from z19_models import Base
from z19_routes import setup_routes

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

# Funkcja tworząca i konfigurująca aplikację aiohttp
async def create_app():
    app = web.Application()
    setup_routes(app)
    app.on_startup.append(init_db)  # inicjalizacja bazy przy starcie aplikacji
    app.on_cleanup.append(close_db) # czyszczenie zasobów przy zamykaniu aplikacji
    return app

# Uruchomienie serwera, jeśli skrypt jest wywołany bezpośrednio
if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)
    
