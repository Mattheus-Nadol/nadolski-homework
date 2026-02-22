"""
Konfiguracja bazy danych dla aplikacji FastAPI (async SQLAlchemy).

W tym pliku:
- konfigurujemy silnik bazy danych (engine)
- tworzymy fabrykę sesji (sessionmaker)
- definiujemy Base dla modeli ORM
- tworzymy dependency get_db do wstrzykiwania sesji do endpointów

Dokumentacja:
Async SQLAlchemy:
https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

FastAPI + SQLAlchemy:
https://fastapi.tiangolo.com/tutorial/sql-databases/
"""

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base

# Add cache_service import
from services.cache_service import cache_service


# ---------------------------------------------------------
# 1. URL połączenia z bazą danych
# ---------------------------------------------------------
# Używamy SQLite w trybie asynchronicznym.
# "sqlite+aiosqlite" oznacza:
# - sqlite jako baza danych
# - aiosqlite jako async driver
#
# Plik bazy danych zostanie utworzony automatycznie.
DATABASE_URL = "sqlite+aiosqlite:///./books.db"


# ---------------------------------------------------------
# 2. Tworzenie silnika (engine)
# ---------------------------------------------------------
# Engine to centralny obiekt SQLAlchemy,
# który zarządza połączeniami z bazą danych.
#
# echo=True powoduje wypisywanie zapytań SQL w konsoli
# (przydatne edukacyjnie i debugowo).
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


# ---------------------------------------------------------
# 3. Tworzenie fabryki sesji
# ---------------------------------------------------------
# async_sessionmaker tworzy nowe sesje do komunikacji z bazą.
#
# expire_on_commit=False oznacza, że po zapisie danych
# obiekt nie zostanie "wyczyszczony" z pamięci.
# Jest to zalecane w aplikacjach FastAPI.
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ---------------------------------------------------------
# 4. Base dla modeli ORM
# ---------------------------------------------------------
# Wszystkie modele ORM będą dziedziczyć po tej klasie.
# Dzięki temu SQLAlchemy wie, jakie klasy reprezentują tabele.

Base = declarative_base()

# ---------------------------------------------------------
# Zadanie 17 – Startup / Shutdown DB Hooks
# ---------------------------------------------------------

from typing import AsyncGenerator

# Import metadata from ORM models
# (ensure tables are created)
async def init_db():
    import os

    # Create required directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Cleanup resources
async def close_db():
    await engine.dispose()

# Lifespan generator for FastAPI (recommended approach)
async def lifespan_db(app) -> AsyncGenerator:
    # Startup
    await init_db()

    # Load cache at startup
    await cache_service.load_cache()

    yield

    # Shutdown
    await cache_service.save_cache()

    await close_db()


# ---------------------------------------------------------
# 5. Dependency Injection – sesja bazy danych
# ---------------------------------------------------------
# Funkcja get_db będzie używana w endpointach jako:
#
# db: AsyncSession = Depends(get_db)
#
# FastAPI:
# - wywoła tę funkcję przy każdym request
# - utworzy nową sesję
# - po zakończeniu requestu automatycznie ją zamknie
#
# To jest poprawny i bezpieczny sposób pracy z bazą danych.
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
