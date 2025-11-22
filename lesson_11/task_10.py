"""Demonstrates Python class inheritance and method resolution order (MRO) 
using multiple inheritance."""
# pylint: disable=too-few-public-methods
class A:
    """Base class providing a generic identity method."""
    def who_am_i(self):
        """Prints the name of the class."""
        print("I am from: Class A")


class B(A):
    """Derived class that overrides identity method from class A."""
    def who_am_i(self):
        """Prints the name of the class."""
        print("I am from: Class B")


class C(A):
    """Derived class that overrides identity method from class A."""
    def who_am_i(self):
        """Prints the name of the class."""
        print("I am from: Class C")


class D(B):
    """Derived class that overrides identity method from class B."""
    def who_am_i(self):
        """Prints the name of the class."""
        print("I am from: Class D")


class E(C):
    """Derived class that overrides identity method from class C."""
    def who_am_i(self):
        """Prints the name of the class."""
        print("I am from: Class E")


class F(D, E):
    """Class demonstrating multiple inheritance and MRO."""

# Expected MRO for class F: F -> D -> B -> E -> C -> A
# Create instance of class F
f = F()
f.who_am_i() # >> I am from: Class D
# Checking MRO:
# 1. .mro()
print("\nMRO for class F:")
print(F.mro())
# >> MRO dla klasy D:
# >> [<class '__main__.F'>, <class '__main__.D'>, <class '__main__.B'>,
# <class '__main__.E'>, <class '__main__.C'>, <class '__main__.A'>,
# <class 'object'>]
