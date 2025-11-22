"""Module for coordinates preview."""
# pylint: disable=too-few-public-methods
class Point():
    """Class that represents point in 2D with attributes x, y"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"The coordinates are ({self.x}, {self.y})"

point_1 = Point(2, 3)
print(point_1)
