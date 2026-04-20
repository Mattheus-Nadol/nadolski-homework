# z19_routes.py
from aiohttp import web
from z19_handlers import create_product, get_products, get_product_by_id, update_product, delete_product

def setup_routes(app: web.Application):
    # Rejestracja wszystkich endpointów CRUD produktów
    app.router.add_post("/products", create_product)
    app.router.add_get("/products", get_products)  # Rejestracja GET /products
    app.router.add_get("/products/{id}", get_product_by_id)  # Rejestracja GET /products/{id}
    app.router.add_put("/products/{id}", update_product)  # Rejestracja PUT /products/{id}
    app.router.add_delete("/products/{id}", delete_product)  # Rejestracja DELETE /products/{id}