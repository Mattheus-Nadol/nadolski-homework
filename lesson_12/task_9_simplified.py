"""Simple bank account module with deposit and withdrawal operations."""
from dataclasses import dataclass

class NoBalanceError(Exception):
    """Raised when balance is insufficient."""


@dataclass
class BankAccount:
    """Bank account supporting deposit and withdrawal."""
    _balance: float

    @property
    def balance(self):
        """Return current account balance."""
        return self._balance

    def deposit(self, amount):
        """Deposit a positive amount to the account."""
        if amount < 0:
            raise ValueError("Cannot use negative value")
        self._balance += amount
        print(f"Successfully deposited '{amount}'", end=" | ")
        print(f"Current balance: '{self._balance}'")

    def withdraw(self, amount):
        """Withdraw a positive amount if sufficient funds exist."""
        if amount < 0:
            raise ValueError("Cannot use negative value")
        if self._balance < amount:
            raise NoBalanceError(f"Insufficient funds. Available balance: '{self._balance}'")
        self._balance -= amount
        print(f"Successfully withdrawn '{amount}'", end=" | ")
        print(f"Current balance: '{self._balance}'")

# NoBalanceError test
try:
    my_account = BankAccount(1000) # Start with 1000
    print(my_account.balance)
    my_account.deposit(1000) # Added 1000
    print(my_account.balance) # Balance 2000
    my_account.withdraw(500) # Withdrawn 500
    print(my_account.balance) # Balance 1500
    my_account.withdraw(3500) # Attempt of withdrawing 3500 NoBalanceError -
    #Insufficient funds. Available balance: '1500'
    #PROGRAM STOPS
except NoBalanceError as e:
    print(e)
except ValueError as e:
    print(e)

# ValueError test
try:
    print(my_account.balance) # Balance remains 1500
    my_account.deposit(-1000) # Attempt of depositing negative value
    print(my_account.balance)
except NoBalanceError as e:
    print(e)
except ValueError as e:
    print(e)
