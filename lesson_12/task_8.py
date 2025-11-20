"""Simple calculator module for basic arithmetic operations.
Using the excercise from lesson 8, task 1"""

from typing import Union

class WrongOperatorError(Exception):
    """Custom exception for invalid arithmetic operator."""

def calculator(a: Union[int, float], b: Union[int,float], operation: str) -> Union[float, None]:
    """Mathematical operation for two numbers with operation selection.
    
    Function takes two numbers and operation string ("+", "-", "*" or "/"),
    then returns the result of the corresponding operation.

    :param a: First number (integer or float).
    :param b: Second number (integer or float).
    :param operation: Mathematical operation symbol (string).
    :return: result of the mathematical operation.
    """
    if operation == "+":
        return a + b
    if operation == "-":
        return a - b
    if operation == "*":
        return a * b
    if operation == "/":
        if b == 0:
            raise ZeroDivisionError
        return a / b
    if operation not in "+-*/":
        raise WrongOperatorError
    return None

while True:
    try:
        a_input = float(input("Enter number A: "))
        b_input = float(input("Enter number B: "))
        CHOICE = str(input("Enter operation (+, -, *, /): "))
        result = calculator(a_input, b_input, CHOICE)
    except ValueError:
        print("Invalid input: please enter numbers only")
    except ZeroDivisionError:
        print("Error: division by zero")
    except WrongOperatorError:
        print("Error: invalid operator")
    else:
        print(f"Result: {result}")
    finally:
        print("Calculation complete")
    break
