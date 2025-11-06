"""Module demonstrating employee salary calculation with inheritance."""
# pylint: disable=too-few-public-methods
class Employee:
    """Base employee class with hourly rate salary calculation."""
    def __init__(self, name, hour_rate):
        self.name = name
        self.hour_rate = hour_rate

    def calculate_salary(self, hours: float) -> str:
        """Calculate total salary based on hours worked and hourly rate.
        param: hours: Number of hours worked (float).
        return: Total salary for the period (float)."""
        return f"Total paycheck: {self.hour_rate * hours} €"

class Programmer(Employee):
    """Programmer: specialized employee with programming language skills."""
    def __init__(self, name, hour_rate, programming_languages):
        self.programming_languages = programming_languages
        super().__init__(name, hour_rate)

employee_1 = Programmer("Andrzej", 50, ["Python", "JavaScript", "SQL"])
print(employee_1.calculate_salary(168.0))
