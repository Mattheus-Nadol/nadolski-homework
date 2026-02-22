"""
Modele ORM (SQLAlchemy) dla aplikacji.

UWAGA:
To NIE są modele Pydantic.
To są klasy mapowane bezpośrednio na tabele w bazie danych.

Różnica:
- ORM model -> reprezentuje tabelę w DB
- Pydantic schema -> reprezentuje dane wejściowe/wyjściowe API

Dokumentacja:
SQLAlchemy ORM:
https://docs.sqlalchemy.org/en/20/orm/

Declarative mapping:
https://docs.sqlalchemy.org/en/20/orm/declarative_mapping.html
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# ---------------------------------------------------------
# Model ORM: Author
# ---------------------------------------------------------
class Author(Base):
    """
    Model ORM reprezentujący autora.

    Każdy autor może mieć wiele książek (relacja 1:N).
    """
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    # Relacja 1:N do książek
    books = relationship(
        "Book", 
        back_populates="author", 
        cascade="all, delete-orphan"
    )


# ---------------------------------------------------------
# Model ORM: Book
# ---------------------------------------------------------
class Book(Base):
    """
    Model ORM reprezentujący tabelę 'books' z relacją do autora.

    Każda instancja odpowiada jednemu wierszowi w tabeli.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # Relacja do autora

    author = relationship("Author", back_populates="books")


# ---------------------------------------------------------
# Model ORM: User (Blog API)
# ---------------------------------------------------------
class User(Base):
    """
    Model ORM reprezentujący użytkownika bloga.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)

    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    comments = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ---------------------------------------------------------
# Model ORM: Post
# ---------------------------------------------------------
class Post(Base):
    """
    Model ORM reprezentujący post blogowy.

    Tylko autor postu powinien mieć prawo do edycji.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="posts")

    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


# ---------------------------------------------------------
# Model ORM: Comment
# ---------------------------------------------------------
class Comment(Base):
    """
    Model ORM reprezentujący komentarz do posta.
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")