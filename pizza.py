from enum import Enum
from decimal import Decimal, getcontext
from typing import List

# class AbstractOptionsEnum(Enum):
#     @classmethod
#     def to_enum(cls, name: str):
#         """Return the enum object that has the given name. Raises KeyError if
#         name is not a valid member of the enum.
#         """
#         print(cls.__members__)
#         if not name.upper() in cls.__members__.keys():
#             raise KeyError(f"'{name}' is not a valid member of {cls}")
#         return cls.__members__[name.upper()]
    
#     def get_name(self) -> str:
#         """Return the name of the current enum member, in lowercase."""
#         return self.name.lower()


class InvalidOptionError(Exception):
    """"""
    def __init__(self, option: str, option_type: str) -> None:
        self.option = option
        self.option_type = option_type

    def __str__(self) -> str:
        return f"{self.option} is not a valid Pizza {self.option_type} option"


class Pizza:
    """ A Pizza with size, type and toppings.
    size      : The size of the Pizza.
    pizza_type: The type of the Pizza.
    toppings  : A list of this Pizza's additional toppings (in addition to the
              toppings that come with the pizza type)
    """

    """ Mapping of pizza sizes to prices."""
    PIZZA_SIZE_TO_PRICE = {
        "SMALL"      : Decimal("0.00"),
        "MEDIUM"     : Decimal("2.00"),
        "LARGE"      : Decimal("4.00"),
        "EXTRA_LARGE": Decimal("6.00")
    }

    """ Mapping of pizza type to prices."""
    PIZZA_TYPE_TO_PRICE = {
        "PEPPERONI"  : Decimal("6.99"),
        "MARGHERITA" : Decimal("7.99"),
        "VEGETARIAN" : Decimal("6.49"),
        "NEAPOLITAN" : Decimal("7.99"),
        "CUSTOM"     : Decimal("5.99")
    }
    
    """ Mapping of additional pizza toppings to prices."""
    PIZZA_TOPPING_TO_PRICE = {
        "OLIVE"       : Decimal("1.00"),
        "TOMATO"      : Decimal("1.00"),
        "MUSHROOM"    : Decimal("1.00"),
        "JALAPENO"    : Decimal("1.00"),
        "CHICKEN"     : Decimal("2.00"),
        "BEEF"        : Decimal("2.00"),
        "PEPPERONI"   : Decimal("1.50"),
        "PINEAPPLE"   : Decimal("1.00"),
        "BACON"       : Decimal("1.50"),
        "EXTRA_CHEESE": Decimal("1.25")
    }
    
    def __init__(self, size: str, toppings: List[str], pizza_type: str) -> None:
        """ Create new Pizza object."""
        self.set_size(size)
        self.set_pizza_type(pizza_type)
        self.set_toppings(toppings)

    def set_size(self, size: str) -> None:
        """ Set the size of this Pizza object as 'size'. Raise
        InvalidOptionError if 'size' is not a valid size option."""
        if size.upper() not in self.PIZZA_SIZE_TO_PRICE:
            raise InvalidOptionError(size, option_type="size")
        self.size = size.upper()
            
    def set_pizza_type(self, pizza_type: str):
        """ Set the type of this Pizza object as pizza_type. Raise
        InvalidOptionError if pizza_type is not a valid type option."""
        if pizza_type.upper() not in self.PIZZA_TYPE_TO_PRICE:
            raise InvalidOptionError(pizza_type, option_type="type")
        self.pizza_type = pizza_type.upper()

    def add_topping(self, topping: str) -> None:
        """Add 'topping' as an additional option for this Pizza. Raise
        InvalidOptionError if 'topping' is not a valid topping option."""
        if topping.upper() not in self.PIZZA_TOPPING_TO_PRICE:
            raise InvalidOptionError(topping, option_type="topping")
        self.toppings.append(topping.upper())

    def remove_topping(self, topping: str) -> None:
        """Remove topping as an additional option for this Pizza, if topping is
        one of the previously selected toppings. Raise InvalidOptionError if
        topping is not a valid topping option."""
        topping_formatted = topping.upper()
        if topping_formatted not in self.PIZZA_TOPPING_TO_PRICE:
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
        return self.size.lower()

    def get_pizza_type(self) -> str:
        """ Returns the pizza type as string."""
        return self.pizza_type.lower()

    def get_toppings(self) -> List[str]:
        """ Returns the list of additional pizza toppings as strings."""
        topping_strings = []
        for topping in self.toppings:
            topping_strings.append(topping.lower())
        return topping_strings

    def get_price(self) -> Decimal:
        """ Returns the price of this Pizza."""
        toppings_total = Decimal("0.00")
        for topping in self.toppings:
            toppings_total += self.PIZZA_TOPPING_TO_PRICE[topping]
        return self.PIZZA_SIZE_TO_PRICE[self.size] \
               + self.PIZZA_TYPE_TO_PRICE[self.pizza_type] + toppings_total


# if __name__ == "__main__":
#     pizza = Pizza("Small", ["Beef", "Chicken"], "Custom")
#     print(pizza.get_size())
#     print(pizza.get_price())
#     print(pizza.get_toppings())