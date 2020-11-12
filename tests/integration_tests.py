import unittest
from decimal import Decimal

import options
from cart import Cart
from drink import Drink
from invalid_option_error import InvalidOptionError
from pizza import Pizza
from PizzaParlour import app
from product import Product

class TestIntegration(unittest.TestCase):
    def setUp(self):
        Drink.set_type_to_price(options.DRINK_TYPE_TO_PRICE)
        Pizza.set_type_to_price(options.PIZZA_TYPE_TO_PRICE)
        Pizza.set_size_to_price(options.PIZZA_SIZE_TO_PRICE)
        Pizza.set_topping_to_price(options.PIZZA_TOPPING_TO_PRICE)

    def test_request(self):
        self.assertTrue(True)