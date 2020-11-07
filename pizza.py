from decimal import Decimal
from typing import Dict, List

from invalid_option_error import InvalidOptionError
from product import Product


class Pizza(Product):
    """ A Pizza with size, type and toppings.
    size      : The size of the Pizza.
    toppings  : A list of this Pizza's additional toppings (in addition to the
                toppings that come with the pizza type)
    """

    @classmethod
    def set_size_to_price(cls, size_to_price: Dict[str, Decimal]) -> None:
        """Set the size_to_price dictionary of the pizza class"""
        cls.size_to_price = size_to_price

    @classmethod
    def set_topping_to_price(cls, topping_to_price: Dict[str, Decimal]) -> None:
        """Set the topping_to_price dictionary of the pizza class"""
        cls.topping_to_price = topping_to_price

    def __init__(self, size: str, toppings: List[str], pizza_type: str) -> None:
        """ Create new Pizza object."""
        super().__init__(pizza_type)
        self.set_size(size)
        self.set_toppings(toppings)

    def set_size(self, size: str) -> None:
        """ Set the size of this Pizza object as 'size'. Raise
        InvalidOptionError if 'size' is not a valid size option."""
        if size.upper() not in self.size_to_price:
            raise InvalidOptionError(size, option_type="size")
        self.size = size.upper()  # use uppercase keys in these dictionaries

    def add_topping(self, topping: str) -> None:
        """Add 'topping' as an additional option for this Pizza. Raise
        InvalidOptionError if 'topping' is not a valid topping option."""
        if topping.upper() not in self.topping_to_price:
            raise InvalidOptionError(topping, option_type="topping")
        self.toppings.append(topping.upper())  # use uppercase keys

    def remove_topping(self, topping: str) -> None:
        """Remove topping as an additional option for this Pizza, if topping is
        one of the previously selected toppings. Raise InvalidOptionError if
        topping is not a valid topping option."""
        topping_formatted = topping.upper()
        if topping_formatted not in self.topping_to_price:
            raise InvalidOptionError(topping, option_type="topping")
        if topping_formatted in self.toppings:
            self.toppings.remove(topping_formatted)

    def set_toppings(self, toppings: List[str]):
        """ Set the additional toppings of this Pizza object as 'toppings'.
        Raise InvalidOptionError if any element of 'toppings' is not a valid
        topping option."""
        self.toppings = []  # Clear any previous choices
        for topping in toppings:
            self.add_topping(topping)

    def get_size(self) -> str:
        """ Returns the pizza size as string."""
        return self.size

    def get_toppings(self) -> List[str]:
        """ Returns the list of additional pizza toppings as strings."""
        topping_strings = []
        for topping in self.toppings:
            topping_strings.append(topping)
        return topping_strings

    def get_price(self) -> Decimal:
        """ Returns the price of this Pizza."""
        toppings_total = Decimal("0.00")
        for topping in self.toppings:
            toppings_total += self.topping_to_price[topping]
        return self.size_to_price[self.size] \
            + self.type_to_price[self.type_] + toppings_total


# if __name__ == "__main__":
#     pizza = Pizza("Small", ["Beef", "Chicken"], "Custom")
#     print(pizza.get_size())
#     print(pizza.get_price())
#     print(pizza.get_toppings())
