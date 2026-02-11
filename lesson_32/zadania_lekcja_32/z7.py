"""
Definicja modelu Product przy użyciu SQLAlchemy Async z DeclarativeBase.
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String

DATABASE_URL = os.environ.get("DB_URL", "postgresql+asyncpg://postgres:postgres@localhost/aio_test_db")

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    price = mapped_column(Integer, nullable=False)  # cena w groszach

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
        }

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)