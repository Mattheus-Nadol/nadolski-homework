"""Safe division helper that returns a float or None on error."""
from typing import Union


def safe_division(a:Union[int, float], b:Union[int, float]) -> Union[float, None]:
    """A function for safe division, takes two arguments (int or float)
    Returns the result of the division (float) or None if an error occurs"""
    try:
        return a / b
    except ZeroDivisionError:
        print("Division by zero - ERROR /", end=" ")
        return None

print(safe_division(3, 4))
print(safe_division(3, 0))
