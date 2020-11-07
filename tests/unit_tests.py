from PizzaParlour import app
from pizza import Pizza, InvalidOptionError
from abstract_product import AbstractProduct
from decimal import Decimal
import unittest

def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'


class TestAbstractProduct(unittest.TestCase):
    def test_get_price(self):
        self.assertRaises(NotImplementedError, AbstractProduct().get_price)


class TestPizza(unittest.TestCase):
    def setUp(self):
        self.pizza = Pizza("Small", ["Beef", "Chicken"], "Custom")
        self.prev_toppings_len = 2

    def test_initial_fields_and_setters(self):
        # Initialization uses all setters
        self.assertEqual(self.pizza.size, "SMALL")
        self.assertEqual(self.pizza.pizza_type, "CUSTOM")
        self.assertTrue("BEEF" in self.pizza.toppings)
        self.assertTrue("CHICKEN" in self.pizza.toppings)
        self.assertEqual(len(self.pizza.toppings), self.prev_toppings_len)

    def test_getters(self):
        self.assertEqual(self.pizza.get_size(), "small")
        self.assertEqual(self.pizza.get_pizza_type(), "custom")
        self.assertEqual(self.pizza.get_toppings(), ["beef", "chicken"])

    def test_set_invalid_size(self):
        self.assertRaises(InvalidOptionError, self.pizza.set_size, "Blabla")
        self.assertEqual(self.pizza.size, "SMALL")

    def test_set_invalid_pizza_type(self):
        self.assertRaises(InvalidOptionError, self.pizza.set_pizza_type, "Blabla")
        self.assertEqual(self.pizza.pizza_type, "CUSTOM")

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
        self.assertRaisesRegex(InvalidOptionError, \
                               "'Blabla' is not a valid Pizza topping option", \
                               self.pizza.remove_topping, \
                               "Blabla")
        self.assertEqual(len(self.pizza.toppings), self.prev_toppings_len)

    def test_get_price(self):
        self.assertEqual(self.pizza.get_price(), Decimal("9.99"))
