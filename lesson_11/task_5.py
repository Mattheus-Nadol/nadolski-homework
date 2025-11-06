"""Simple geometry module with Figure, Square and Circle classes.

Each class implements a calculate_area method (here returning a
formatted string)."""
# pylint: disable=too-few-public-methods
class Figure:
    """Base figure class: subclasses should implement calculate_area."""
    def calculate_area(self):
        """Subclasses must override this method and return an area."""
        raise NotImplementedError("Subclasses must implement calculate_area")

class Square(Figure):
    """Square defined by its side length `a`."""
    def __init__(self, a):
        self.a = a
    def calculate_area(self):
        """Return a formatted string with the square area."""
        return f"Square area with side = {self.a} is: {self.a ** 2}"

class Circle(Figure):
    """Circle defined by its radius `r`."""
    def __init__(self, r):
        self.r = r
    def calculate_area(self):
        """Return a formatted string with the circle area."""
        PI = 3.14159
        return f"Circle area with radius = {self.r} is: {PI * self.r ** 2}"

square_1 = Square(2)
circle_1 = Circle(2)
figures = [square_1, circle_1]
for figure in figures:
    print(figure.calculate_area())
