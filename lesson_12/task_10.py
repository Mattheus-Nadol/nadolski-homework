"""Metaclass exercise: validate that non-magic methods have docstrings.

This module provides a metaclass that raises TypeError when a class is
created whose methods (excluding magic methods) lack a docstring. It also
demonstrates correct and incorrect uses.
"""

from types import FunctionType


class MetaValidateMethods(type):
    """Metaclass that enforces docstrings on non-magic methods."""

    def __new__(mcs, name, bases, dct):
        """Validate that non-magic methods defined on the class have docstrings.

        Raises TypeError naming the first method found without a docstring.
        """
        # iterate over attributes declared directly in the class body
        for attr_name, attr_value in dct.items():
            # skip magic / dunder names
            if attr_name.startswith("__"):
                continue

            # unwrap classmethod/staticmethod to get the underlying function
            func = None
            if isinstance(attr_value, (classmethod, staticmethod)):
                func = attr_value.__func__
            elif isinstance(attr_value, FunctionType):
                func = attr_value
            else:
                # not a plain method (could be property, descriptor, data), skip
                continue

            # At this point func is the function object implementing the method
            doc = getattr(func, "__doc__", None)
            if not doc or not doc.strip():
                raise TypeError(f"Method '{attr_name}' in class '{name}' must have a docstring")

        return super().__new__(mcs, name, bases, dct)


# --- Demonstration classes ---

class MyFirstClass(metaclass=MetaValidateMethods):
    """A class with properly documented methods."""

    def my_first_method(self):
        """This is my first method."""
        print("This is my first method")


# The following class definition is wrapped in try/except so the example
# demonstrates the metaclass raising a TypeError without stopping the module.
try:
    class MySecondClass(metaclass=MetaValidateMethods):
        """A class missing method docstrings (should trigger TypeError)."""

        def my_second_method(self):
            # no docstring here -> metaclass should raise
            print("This is my second method")
except TypeError as err:
    print("TypeError raised as expected when creating MySecondClass:", err)
