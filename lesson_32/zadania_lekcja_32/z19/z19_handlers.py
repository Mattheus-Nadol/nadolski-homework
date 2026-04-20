"""
Moduł zawiera wszystkie handlery do CRUD produktów.
"""

from aiohttp import web
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from z19_models import Product


async def create_product(request: web.Request) -> web.Response:
    """Handler do tworzenia nowego produktu (POST /products)."""
    data = await request.json()
    async with request.app["db_session_factory"]() as session:
        # Tworzymy nowy obiekt produktu z danych z requestu
        new_product = Product(**data)
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        # Zwracamy utworzony produkt z kodem 201
        return web.json_response(new_product.to_dict(), status=201)


async def get_products(request: web.Request) -> web.Response:
    """Handler do pobierania listy produktów z paginacją (GET /products)."""
    page = int(request.query.get("page", 1))
    limit = int(request.query.get("limit", 10))
    offset = (page - 1) * limit
    async with request.app["db_session_factory"]() as session:
        # Tworzymy zapytanie z paginacją
        stmt = select(Product).offset(offset).limit(limit)
        result = await session.execute(stmt)
        products = result.scalars().all()
        # Zwracamy listę produktów jako JSON
        return web.json_response([p.to_dict() for p in products])


async def get_product_by_id(request: web.Request) -> web.Response:
    """Handler do pobierania pojedynczego produktu po id (GET /products/{id})."""
    product_id = int(request.match_info["id"])
    async with request.app["db_session_factory"]() as session:
        stmt = select(Product).where(Product.id == product_id)
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()
        if product is None:
            # Produkt nie znaleziony - zwracamy 404
            raise web.HTTPNotFound(text=f"Product with id {product_id} not found")
        # Zwracamy znaleziony produkt
        return web.json_response(product.to_dict())


async def update_product(request: web.Request) -> web.Response:
    """Handler do aktualizacji produktu po id (PUT /products/{id})."""
    product_id = int(request.match_info["id"])
    data = await request.json()
    async with request.app["db_session_factory"]() as session:
        stmt = select(Product).where(Product.id == product_id)
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()
        if product is None:
            # Produkt nie znaleziony - zwracamy 404
            raise web.HTTPNotFound(text=f"Product with id {product_id} not found")
        # Aktualizujemy pola produktu z danych z requestu
        for key, value in data.items():
            setattr(product, key, value)
        session.add(product)
        await session.commit()
        await session.refresh(product)
        # Zwracamy zaktualizowany produkt
        return web.json_response(product.to_dict())


async def delete_product(request: web.Request) -> web.Response:
    """Handler do usuwania produktu po id (DELETE /products/{id})."""
    product_id = int(request.match_info["id"])
    async with request.app["db_session_factory"]() as session:
        stmt = select(Product).where(Product.id == product_id)
        result = await session.execute(stmt)
        product = result.scalar_one_or_none()
        if product is None:
            # Produkt nie znaleziony - zwracamy 404
            raise web.HTTPNotFound(text=f"Product with id {product_id} not found")
        # Usuwamy produkt z bazy
        await session.delete(product)
        await session.commit()
        # Zwracamy odpowiedź 204 No Content
        return web.Response(status=204)
