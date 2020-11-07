from decimal import Decimal
from typing import Dict

from invalid_option_error import InvalidOptionError


class Product:
    """An class for products in the pizzeria system.
    type_: The type of the Product.
    """

    @classmethod
    def set_type_to_price(cls, type_to_price: Dict[str, Decimal]) -> None:
        """Set the type_to_price dictionary of this product class"""
        cls.type_to_price = type_to_price

    def __init__(self, type_) -> None:
        """Initialize a product object."""
        self.set_type(type_)

    def set_type(self, type_: str) -> None:
        """ Set the type of this product as 'type_'. Raise
        InvalidOptionError if 'type_' is not a valid type option."""
        if type_.upper() not in self.type_to_price:
            raise InvalidOptionError(type_, option_type="type")
        self.type_ = type_.upper()  # use uppercase keys in these dictionaries

    def get_type(self) -> str:
        """ Returns the product type as a string."""
        return self.type_

    def get_price(self) -> Decimal:
        """Return the price of this product. This is an abstract method."""
        raise NotImplementedError()
