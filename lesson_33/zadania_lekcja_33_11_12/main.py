from fastapi import FastAPI, Path, Query, HTTPException, Header, Depends
from datetime import datetime
import random
from typing import Union
from models.models import Product, Book, User
from routers import books, authors

app = FastAPI(title="LearnIT FastAPI Exercises", description="API do zadań z lekcji 33")


# (33) Zadanie 10 - Dependency do weryfikacji API key
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "secret-key":
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


# (33) Zadanie 1
@app.get("/", tags=["Basics"])
async def root():
    """
    Endpoint rootowy zwracający prostą wiadomość powitalną.

    Przykład wywołania:
    GET /

    Przykładowa odpowiedź:
    {
        "message": "Hello"
    }
    """
    return {"message": "Hello"}


@app.get("/time", tags=["Basics"])
async def get_time():
    """
    Endpoint zwracający aktualny czas serwera.

    Przykład wywołania:
    GET /time

    Przykładowa odpowiedź:
    {
        "current_time": "2024-06-01T12:34:56.789123"
    }
    """
    current_time = datetime.now()
    return {"current_time": current_time}


@app.get("/random", tags=["Basics"])
async def get_random_number():
    """
    Endpoint zwracający losową liczbę całkowitą z zakresu 1-100.

    Przykład wywołania:
    GET /random

    Przykładowa odpowiedź:
    {
        "random_number": 42
    }
    """
    number = random.randint(1, 100)
    return {"random_number": number}


# (33) Zadanie 2
@app.get("/greet/{name}", tags=["Greetings"], dependencies=[Depends(verify_api_key)])
async def greet(name: str = Path(..., min_length=2)): 
    """
    Endpoint zwracający powitanie dla podanego imienia.

    Przykład wywołania:
    GET /greet/Jan

    Przykładowa odpowiedź:
    {
        "message": "Hello Jan"
    }
    """
    # ... - obiekt Ellipsis, wartość wymagana
    return {"message": f"Hello {name}"}


# (33) Zadanie 3
@app.get("/calculate", tags=["Calculator"], dependencies=[Depends(verify_api_key)])
async def calculate(
    a: Union[int | float] = Query(..., description="Pierwsza liczba"),
    b: Union[int | float] = Query(..., description="Druga liczba"),
    operation: str = Query("add", description="Operacja: add, subtract, multiply, divide")
): 
    """
    Endpoint wykonujący prostą operację matematyczną na dwóch liczbach.

    Wymaga nagłówka: X-API-Key

    Przykład wywołania:
    GET /calculate?a=5&b=3&operation=add

    Przykładowa odpowiedź:
    {
        "a": 5,
        "b": 3,
        "operation": "add",
        "result": 8
    }
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise HTTPException(status_code=400, detail="Nie można dzielić przez zero")
        result = a / b
    else:
        raise HTTPException(status_code=400, detail="Nieznana operacja")
    
    return {"a": a, "b": b, "operation": operation, "result": result}


# (33) Zadanie 4 - endpoint
@app.post("/products", tags=["Products"], dependencies=[Depends(verify_api_key)])
async def create_product(product: Product):
    """
    Endpoint do tworzenia produktu i obliczania jego łącznej ceny.

    Wymaga nagłówka: X-API-Key

    Przykład wywołania:
    POST /products
    Body:
    {
        "name": "Mleko",
        "price": 2.5,
        "quantity": 4
    }

    Przykładowa odpowiedź:
    {
        "name": "Mleko",
        "price": 2.5,
        "quantity": 4,
        "total_price": 10.0
    }
    """
    total_price = product.price * product.quantity
    return {
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
        "total_price": total_price
    }


# (33) Zadanie 9 - routery (endpointy z Zadania 5 w pliku routers/books.py)
app.include_router(books.router)
app.include_router(authors.router)

# (33) Zadanie 7 - endpoint
@app.post("/users", tags=["Users"])
async def create_user(user: User):
    """
    Endpoint do tworzenia nowego użytkownika.

    Przykład wywołania:
    POST /users
    Body:
    {
        "email": "janek@example.com"
    }

    Przykładowa odpowiedź:
    {
        "email": "janek@example.com"
    }
    """
    return user
