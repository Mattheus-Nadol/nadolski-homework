"""Simple calculator module for basic arithmetic operations.

This module defines a Calculator class that performs basic arithmetic
operations (+, -, *, /) with full error handling. It interacts with the user
via the console and continues running until the user decides to exit.
"""
from typing import Union

class WrongOperatorError(Exception):
    """Custom exception for invalid arithmetic operator."""

class Calculator:
    """Calculator class to perform basic arithmetic operations with user interaction."""
    def __init__(self, a: Union[int, float], b: Union[int,float], operation: str) -> None:
        """Initializes the calculator with two numbers and an operation."""
        self.a = a
        self.b = b
        self.operation = operation

    def calculate(self):
        """Performs the arithmetic operation and returns the result."""
        if self.operation == "+":
            return self.a + self.b
        if self.operation == "-":
            return self.a - self.b
        if self.operation == "*":
            return self.a * self.b
        if self.operation == "/":
            if self.b == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return self.a / self.b
        return None

    def run(self):
        """Handles the interactive loop for user input, calculation, and graceful error handling."""
        while True:
            self.get_input()
            try:
                result = self.calculate()
            except ZeroDivisionError as e:
                print(e)
            else:
                print("Result:", result)
            finally:
                print("Calculation complete")
            user_choice = input("Would you like to continue (y/n): ")
            if user_choice.lower().strip() == "y":
                continue
            break

    def get_input(self):
        """Prompts the user for input values and validates the arithmetic operator."""
        while True:
            try:
                self.a = float((input("Enter number A: ")).strip())
                self.b = float((input("Enter number B: ")).strip())
                self.operation = str((input("Enter operation (+, -, *, /): ")).strip())
                if self.operation not in "+-*/":
                    raise WrongOperatorError("Invalid operator")
            except (TypeError, ValueError) as e:
                print(e)
                continue
            except WrongOperatorError as e:
                print(e)
                continue
            break

if __name__ == "__main__":
    user_calculation = Calculator(0, 0, "+")
    user_calculation.run()
