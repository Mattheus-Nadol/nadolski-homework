"""Simple date helper with a Data container and parsing constructor."""
# pylint: disable=too-few-public-methods
class Data:
    """Container for day, month and year fields."""
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, formatted_date):
        """Create a Data instance from a 'DD-MM-YYYY' formatted string."""
        our_date = formatted_date.split("-")
        # print(our_date)
        return cls(our_date[0], our_date[1], our_date[2])

test_1 = Data.from_string("03-11-2025")
print(test_1)
print(test_1.day)
print(test_1.month)
print(test_1.year)
