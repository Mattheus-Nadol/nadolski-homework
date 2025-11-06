"""Module for validating user registration data using custom rules"""
# pylint: disable=too-few-public-methods
class UserRegistration:
    """Class for handling user registration with email and password validation"""
    def __init__(self, email, password):
        """Initialize user with validated email and password"""
        if "@" not in email or "." not in email:
            raise ValueError("Incorrect email")
        self.email = email
        if len(password) < 8:
            raise ValueError("Password too short")
        self.password = password

    def __str__(self):
        """Return a formatted string confirming approved registration"""
        return f"Email '{self.email}' and password '{self.password}' APPROVED"


try:
    user_email = input("Enter email: ")
    user_password = input("Enter password: ")
    user_data = UserRegistration(user_email, user_password)
    print(user_data)
except ValueError as e:
    print("An error occured:", e)
