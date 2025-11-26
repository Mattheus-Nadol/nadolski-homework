# sqlalchemy_app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///todo_orm.db"

engine = create_engine(DATABASE_URL) # Silnik łączący się z bazą
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Generator sesji bazy danych."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
