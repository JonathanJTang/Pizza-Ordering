import unittest
from decimal import Decimal

import options
from drink import Drink
from invalid_option_error import InvalidOptionError
from pizza import Pizza
from PizzaParlour import app
from product import Product


def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'


class TestProduct(unittest.TestCase):
    def setUp(self):
        Product.set_type_to_price({"A": 0, "B": 1})
        self.product = Product("A")

    def test_get_type(self):
        self.assertEqual(self.product.get_type(), "A")

    def test_set_invalid_type(self):
        self.assertRaises(InvalidOptionError, self.product.set_type, "Blabla")
        self.assertEqual(self.product.type_, "A")

    def test_get_price(self):
        self.assertRaises(NotImplementedError, self.product.get_price)


class TestPizza(unittest.TestCase):
    def setUp(self):
        Pizza.set_type_to_price(options.PIZZA_TYPE_TO_PRICE)
        Pizza.set_size_to_price(options.PIZZA_SIZE_TO_PRICE)
        Pizza.set_topping_to_price(options.PIZZA_TOPPING_TO_PRICE)
        self.pizza = Pizza("Small", ["Beef", "Chicken"], "Custom")
        self.prev_toppings_len = 2

    def test_initial_fields_and_setters(self):
        # Initialization uses all setters
        self.assertEqual(self.pizza.size, "SMALL")
        self.assertTrue("BEEF" in self.pizza.toppings)
        self.assertTrue("CHICKEN" in self.pizza.toppings)
        self.assertEqual(len(self.pizza.toppings), self.prev_toppings_len)

    def test_getters(self):
        self.assertEqual(self.pizza.get_size(), "SMALL")
        self.assertEqual(self.pizza.get_toppings(), ["BEEF", "CHICKEN"])

    def test_set_invalid_size(self):
        self.assertRaises(InvalidOptionError, self.pizza.set_size, "Blabla")
        self.assertEqual(self.pizza.size, "SMALL")

    def test_add_topping(self):
        self.pizza.add_topping("Olive")
        self.assertTrue("OLIVE" in self.pizza.toppings)
        self.assertEqual(len(self.pizza.toppings), self.prev_toppings_len + 1)

    def test_add_invalid_topping(self):
        self.assertRaises(InvalidOptionError, self.pizza.add_topping, "Blabla")
        self.assertEqual(len(self.pizza.toppings), self.prev_toppings_len)

    def test_remove_existing_topping(self):
        self.pizza.remove_topping("Beef")
        self.assertTrue("BEEF" not in self.pizza.toppings)
        self.assertEqual(len(self.pizza.toppings), self.prev_toppings_len - 1)

    def test_remove_nonexistent_topping(self):
        self.pizza.remove_topping("Olive")
        self.assertEqual(len(self.pizza.toppings), self.prev_toppings_len)

    def test_remove_invalid_topping(self):
        self.assertRaisesRegex(InvalidOptionError,
                               "'Blabla' is not a valid Pizza topping option",
                               self.pizza.remove_topping,
                               "Blabla")
        self.assertEqual(len(self.pizza.toppings), self.prev_toppings_len)

    def test_get_price(self):
        self.assertEqual(self.pizza.get_price(), Decimal("9.99"))


class TestDrink(unittest.TestCase):
    def setUp(self):
        Drink.set_type_to_price(options.DRINK_TYPE_TO_PRICE)
        self.drink = Drink("Juice")

    def test_initial_fields_and_setters(self):
        self.drink.set_type("Juice")
        self.assertEqual(self.drink.type_, "JUICE")

    def test_getters(self):
        self.assertEqual(self.drink.get_type(), "JUICE")

    def test_getprice(self):
        self.assertEqual(self.drink.get_price(), Decimal("3.01"))
