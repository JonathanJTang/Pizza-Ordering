from decimal import Decimal
from product import Product


class Drink(Product):
    """ A drink with type.
    """

    def __init__(self, drink_type: str) -> None:
        """ Create new Drink object."""
        super().__init__(drink_type)

    def get_price(self) -> Decimal:
        """ Returns the price of this Drink."""
        return self.type_to_price[self.type_]
