# (33) Zadanie 4 - model
from pydantic import BaseModel, Field, EmailStr # pip install email-validator

class Product(BaseModel):
    name: str = Field(..., min_length=1, description="Nazwa produktu")
    price: float = Field(..., gt=0, description="Cena produktu (większa niż 0)")
    quantity: int = Field(..., ge=0, description="Ilość produktu (nieujemna)")

# (33) Zadanie 5 - model
class Book(BaseModel):
    title: str
    author: str
    pages: int

# (33) Zadanie 7 - model
class User(BaseModel):
    email: EmailStr