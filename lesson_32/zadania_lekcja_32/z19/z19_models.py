"""Plik zawiera modele dla CRUD produktów."""

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String, Float

# Definicja bazowej klasy dla modeli SQLAlchemy
class Base(DeclarativeBase):
    pass

# Definicja modelu Product reprezentującego produkt w bazie danych
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # Klucz główny
    name: Mapped[str] = mapped_column(String(100))  # Nazwa produktu
    price: Mapped[float] = mapped_column(Float)  # Cena produktu
