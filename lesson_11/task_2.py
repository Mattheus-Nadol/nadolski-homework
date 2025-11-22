"""Short module: simple Product class example."""
# pylint: disable=too-few-public-methods
class Product:
    """Product: holds name, price and category."""
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

user_product = Product("MacBook Air M4", "1299€", "Electronics")
print("Product:", user_product.name)
print("Price:", user_product.price)
print("Category:", user_product.category)
