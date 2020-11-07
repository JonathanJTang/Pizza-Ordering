from decimal import Decimal
from product import Product
from typing import Dict, List, Union

from invalid_option_error import InvalidOptionError


class Drink(Product):
    """ A drink with type.
    """

    def __init__(self, drink_type: str) -> None:
        """ Create new Drink object."""
        super().__init__(drink_type)

    def get_price(self) -> Decimal:
        """ Returns the price of this Drink."""
        return self.type_to_price[self.type_]

    def edit(self, changes: Dict[str, Union[str, List[str]]]) -> None:
        """Edit this Drink with the changes specified in changes. If any of
        the changes are invalid, raise the appropriate error."""
        # Check for invalid variable types in this function; the corresponding
        # setters check whether their values are valid
        for option in changes:
            if not isinstance(option, str):
                raise InvalidOptionError(option, option_type="Drink edit")
            if option.lower() == "type" and isinstance(changes[option], str):
                self.set_type(changes[option])
            else:
                raise InvalidOptionError(option, option_type="Drink edit")
