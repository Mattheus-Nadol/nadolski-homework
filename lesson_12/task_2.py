"""Module defining a simple User class with a validated `age` property.

The `User` class stores a protected `_age` attribute and exposes an
`age` property that enforces values between 0 and 120.
"""
# pylint: disable=too-few-public-methods
class User:
    """User that stores a protected `_age` and exposes a validated `age` property."""
    def __init__(self, age):
        self._age = age

    @property
    def age(self):
        """Return the current age value."""
        return self._age

    @age.setter
    def age(self, updated_age):
        """Set `age` if `updated_age` is between 0 and 120; otherwise print an error."""
        if 0 <= updated_age <= 120:
            self._age = updated_age
        else:
            print("Invalid age")

user1 = User(230)
print(f"Current age: {user1.age}")
user1.age = 45
print(f"Updated age: {user1.age}")
user1.age = 130 # No change, since the condition is not met.
print(f"Invalid age: {user1.age}")
