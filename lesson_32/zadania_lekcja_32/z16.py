"""
Ten skrypt pokazuje transakcję między kontami przy użyciu SQLAlchemy Async i aiohttp.
Dokumentacja SQLAlchemy Async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
Dokumentacja aiohttp: https://docs.aiohttp.org/en/stable/
"""

import os
import asyncio
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import select

DB_URL = os.getenv("DB_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/aio_test_db")

# Definicja bazy i modeli
class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column()

# Tworzenie silnika i fabryki sesji
engine = create_async_engine(DB_URL, echo=False, future=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def init_db(app):
    # Tworzymy tabele w bazie danych przy starcie aplikacji
    # 1. Tabele są tworzone przy starcie aplikacji (Base.metadata.create_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Seeder sprawdza, czy konta już istnieją, więc przy kolejnych uruchomieniach nie będzie dodawał duplikatów
    async with async_session_factory() as session:
        async with session.begin():
            # Sprawdzamy czy konta już istnieją, aby nie dublować
            result = await session.execute(select(Account))
            accounts_exist = result.scalars().first()
            if not accounts_exist:
                # 3. Jeśli konta istnieją, nic się nie robi
                account1 = Account(id=1, balance=1000)
                account2 = Account(id=2, balance=500)
                session.add_all([account1, account2])

    app["db_session_factory"] = async_session_factory

async def close_db(app):
    # Zamykamy silnik bazy danych przy zamykaniu aplikacji
    await engine.dispose()

async def transfer_handler(request):
    # Pobieramy sesję z aplikacji
    session_factory = request.app["db_session_factory"]

    # Parsujemy dane JSON z żądania
    data = await request.json()
    from_id = data.get("from_id")
    to_id = data.get("to_id")
    amount = data.get("amount")

    if not all(isinstance(x, int) for x in (from_id, to_id, amount)):
        return web.json_response({"error": "Nieprawidłowe dane wejściowe"}, status=400)
    if amount <= 0:
        return web.json_response({"error": "Kwota musi być większa od zera"}, status=400)

    async with session_factory() as session:
        try:
            # Rozpoczynamy transakcję
            async with session.begin():
                # Pobieramy oba konta z bazy
                stmt = select(Account).where(Account.id.in_([from_id, to_id]))
                result = await session.execute(stmt)
                accounts = {acc.id: acc for acc in result.scalars()}

                if from_id not in accounts or to_id not in accounts:
                    return web.json_response({"error": "Nie znaleziono jednego z kont"}, status=404)

                from_acc = accounts[from_id]
                to_acc = accounts[to_id]

                # Sprawdzamy czy konto nadawcy ma wystarczające środki
                if from_acc.balance < amount:
                    return web.json_response({"error": "Niewystarczające środki"}, status=400)

                # Aktualizujemy salda kont
                from_acc.balance -= amount
                to_acc.balance += amount

                # Zmiany zostaną automatycznie zatwierdzone po wyjściu z bloku 'begin'

            # Zwracamy zaktualizowane salda
            return web.json_response({
                "from_account": {"id": from_acc.id, "balance": from_acc.balance},
                "to_account": {"id": to_acc.id, "balance": to_acc.balance},
            })

        except Exception as e:
            # W przypadku błędu transakcja zostanie wycofana automatycznie
            return web.json_response({"error": str(e)}, status=500)

def create_app():
    # Tworzymy aplikację aiohttp i rejestrujemy endpointy oraz eventy start/stop
    app = web.Application()
    app.router.add_post("/transfer", transfer_handler)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)
