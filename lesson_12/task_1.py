"""Dataclass examples for lesson 12, task 1.

Defines a Film dataclass used in simple printing examples.
"""
from dataclasses import dataclass

@dataclass
class Film:
    """Film dataclass holding title, director and year."""
    title: str
    director: str
    year: int

movie_a = Film("Twilight", "Chris Weitz", 2008)
movie_b = Film("Matrix", "Lana and Lily Wachowsky", 1999)
print(movie_a)
print(movie_b)
