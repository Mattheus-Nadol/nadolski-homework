"""Module with a tiny currency conversion helper."""
# pylint: disable=too-few-public-methods
class CurrencyCalculator:
    """Simple currency conversion helper with static conversion methods."""
    @staticmethod
    def usd_to_pln(amount_usd):
        """Convert an amount in USD to PLN using a fixed exchange rate."""
        usd_rate_in_pln = 4.0 #Constants in UPPERCASE are accepted by Pylint only in global scope
        return amount_usd * usd_rate_in_pln


result = CurrencyCalculator.usd_to_pln(14)
print(result)
