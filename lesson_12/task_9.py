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
            raise ValueError
        self._balance += amount
        print(f"Successfully deposited '{amount}'", end=" | ")
        print(f"Current balance: '{self._balance}'")

    def withdraw(self, amount):
        """Withdraw a positive amount if sufficient funds exist."""
        if amount < 0:
            raise ValueError
        if self._balance < amount:
            raise NoBalanceError(f"Insufficient funds. Available balance: '{self._balance}'")
        self._balance -= amount
        print(f"Successfully withdrawn '{amount}'", end=" | ")
        print(f"Current balance: '{self._balance}'")

# Module-level account instance used by the helper functions below.
MY_ACCOUNT = None

def set_balance() -> None:
    """Create a BankAccount by setting the initial balance."""
    global MY_ACCOUNT
    balance_input = float(input("Please type your balance: "))
    MY_ACCOUNT = BankAccount(balance_input)
    print(f"Your current balance is: {MY_ACCOUNT.balance}")

def set_deposit() -> None:
    """Prompt for deposit amount and apply it to the account."""
    if MY_ACCOUNT is None:
        print("No account set. Please set your balance first.")
        return
    deposit_input = float(input("How much would you like to deposit: "))
    MY_ACCOUNT.deposit(deposit_input)

def set_withdrawal() -> None:
    """Prompt for withdrawal amount and apply it to the account."""
    if MY_ACCOUNT is None:
        print("No account set. Please set your balance first.")
        return
    withdrawal_input = float(input("How much would you like to withdraw: "))
    MY_ACCOUNT.withdraw(withdrawal_input)

print("*"*20)
print("Welcome to Python Bank Manager")
print("*"*20)
while True:
    print("Available options (0 - set your balance, " \
    "1 - deposit, 2 - withdrawal, 'Enter' or anything else to EXIT)")
    user_input = input("Choose your option: ")
    # any input other than the supported options exits the program
    if user_input not in ("0", "1", "2"):
        print("Thank you for using the Python Bank")
        break
    try:
        if user_input == "0":
            set_balance()
        elif user_input == "1":
            set_deposit()
        elif user_input == "2":
            set_withdrawal()
    except ValueError:
        print("Incorrect amount error")
    except NoBalanceError as e:
        print(f"Balance error: {e}")
