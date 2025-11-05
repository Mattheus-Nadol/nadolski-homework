"""Module: simple Film class example."""
# pylint: disable=too-few-public-methods
class Film:
    """Film: stores title, director and release year."""
    def __init__(self, title, director, year):
        self.title = title
        self.director = director
        self.year = year

    def information(self):
        """Function returns information about the film in the desired format"""
        return f"'{self.title}' ({self.year}), directed by: {self.director}"

movie_a = Film("Twilight", "Chris Weitz", "2008")
movie_b = Film("Matrix", "Lana and Lily Wachowsky", "1999")

print(movie_a.information())
print(movie_b.information())
