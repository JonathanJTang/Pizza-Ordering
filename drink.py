from decimal import Decimal
from typing import Dict

from invalid_option_error import InvalidOptionError
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

    def edit(self, changes: Dict[str, str]) -> None:
        """Edit this Drink with the changes specified in changes. If any of
        the changes are invalid, raise the appropriate error.
        Precondition: changes is a dictionary with one key-value pair of type
        str, where the key is 'type'.
        """
        # The corresponding setter checks whether the values are valid
        for option in changes:
            if option.lower() == "type":
                self.set_type(changes[option])
            else:
                raise InvalidOptionError(
                    Drink.__name__, option, option_type="Drink edit")
