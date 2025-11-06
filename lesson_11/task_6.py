"""Defines a 2D vector class with basic arithmetic and comparison operations."""
class Vector2D:
    """Represents a 2D vector with x and y components and supports basic operations."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector: ({self.x}, {self.y})"

    def __add__(self, other):
        """
        Adds two 2D vectors.
    
        Formula:
            (x1, y1) + (x2, y2) = (x1 + x2, y1 + y2)
    
        Returns:
            A new vector object representing the sum of the two vectors.
        """
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        """
        Subtracts one 2D vector from another.
    
        Formula:
            (x1, y1) - (x2, y2) = (x1 - x2, y1 - y2)
    
        Returns:
            A new vector object representing the difference between the two vectors.
        """
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __eq__(self, other):
        """
        Compares two 2D vectors for equality.
    
        Formula:
            (x1, y1) == (x2, y2) if x1 == x2 and y1 == y2
    
        Returns:
            True if both vectors have the same coordinates, False otherwise.
        """
        if self.x == other.x and self.y == other.y:
            return True
        return False

print("\n1. First example - different vectors")
vector_v = Vector2D(3, -1)
vector_u = Vector2D(2, 2)

print("V", vector_v)
print("U", vector_u)

vector_sum = vector_v + vector_u
print(f"Vectors sum: {vector_sum}")

vector_sub = vector_v - vector_u
print(f"Vectors sub: {vector_sub}")

are_equal = vector_v == vector_u
print(f"The vectors are equal: {are_equal}")

print("\n2. Second example - same vectors")
vector_a = Vector2D(2, 2)
vector_b = Vector2D(2, 2)

print("A", vector_a)
print("B", vector_b)

vector_sum = vector_a + vector_b
print(f"Vectors sum: {vector_sum}")

vector_sub = vector_a - vector_b
print(f"Vectors sub: {vector_sub}")

are_equal = vector_a == vector_b
print(f"The vectors are equal: {are_equal}")
