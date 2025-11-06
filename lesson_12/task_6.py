"""Module demonstrating a custom exception used for password validation."""
class InvalidPasswordError(Exception):
    """Exception raised when password is invalid."""

def set_password(password: str) -> str:
    """Validate password length; raise InvalidPasswordError if too short.

    Returns a confirmation string when accepted.
    """
    if len(password) < 8:
        raise InvalidPasswordError("Password's length is less than 8")
    return "Password approved"

try:
    user_password = input("Type your password: ")
    print(set_password(user_password))
except InvalidPasswordError as e:
    print(f"Password validation error: {e}")
