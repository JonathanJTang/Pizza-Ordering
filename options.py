from decimal import Decimal

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

""" Mapping of drink type to prices."""
DRINK_TYPE_TO_PRICE = {
    "COKE"       : Decimal("2.00"),
    "DIET COKE"  : Decimal("2.50"),
    "COKE ZERO"  : Decimal("2.50"),
    "PEPSI"      : Decimal("2.00"),
    "DIET PEPSI" : Decimal("2.50"),
    "DR PEPPER"  : Decimal("3.00"),
    "WATER"      : Decimal("1.00"),
    "JUICE"      : Decimal("3.01")
}