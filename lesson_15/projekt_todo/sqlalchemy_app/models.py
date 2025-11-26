# sqlalchemy_app/models.py
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base() # Klasa bazowa dla naszych modeli

class Zadanie(Base):
    __tablename__ = 'zadania' # Nazwa tabeli w bazie danych

    id = Column(Integer, primary_key=True)
    opis = Column(String, nullable=False)
    zrobione = Column(Boolean, default=False, nullable=False)
    data_utworzenia = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    tagi = relationship("Tag", secondary="zadanie_tag", back_populates="zadania")

    def __repr__(self):
        return f"<Zadanie(id={self.id}, opis='{self.opis}', zrobione={self.zrobione})>"


class Tag(Base):
    __tablename__ = 'tagi'

    id = Column(Integer, primary_key=True)
    nazwa = Column(String, nullable=False)
    zadania = relationship("Zadanie", secondary="zadanie_tag", back_populates="tagi")

    def __repr__(self):
        return f"<Tag(id={self.id}, nazwa='{self.nazwa}')>"

zadanie_tag = Table(
    "zadanie_tag", Base.metadata,
    Column("zadanie_id", ForeignKey("zadania.id"), primary_key=True),
    Column("tag_id", ForeignKey("tagi.id"), primary_key=True)
    )
