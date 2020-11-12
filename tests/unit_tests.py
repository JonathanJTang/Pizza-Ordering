import unittest
from decimal import Decimal

import options
from cart import Cart
from delivery_method import DeliveryMethod
from drink import Drink
from foodora_delivery import FoodoraDelivery
from invalid_option_error import InvalidOptionError
from json_parser import JsonParser
from order import Order
from order_parser import OrderParser
from pickup import Pickup
from pizza import Pizza
from PizzaParlour import app
from pizzeria_delivery import PizzeriaDelivery
from product import Product
from uber_eats_delivery import UberEatsDelivery
from csv_parser import CsvParser

# JSON data sample for Uber Eats
sample_json = {
    "products": [
        {
            "product_category": "pizza",
            "size": "small",
            "type": "custom",
            "toppings": [
                "olive",
                "chicken"
            ]
        },
        {
            "product_category": "drink",
            "type": "coke"
        }
    ],
    "delivery_method": {
        "type": "pizzeria",
        "details": {
            "address": "74 random street",
            "order_no": 1
        }
    }
}


def setup_options():
    Pizza.set_topping_to_price(options.PIZZA_TOPPING_TO_PRICE)
    Pizza.set_size_to_price(options.PIZZA_SIZE_TO_PRICE)
    Pizza.set_type_to_price(options.PIZZA_TYPE_TO_PRICE)
    Drink.set_type_to_price(options.DRINK_TYPE_TO_PRICE)


def test_pizza():
    response = app.test_client().get('/pizza')

    assert response.status_code == 200
    assert response.data == b'Welcome to Pizza Planet!'


class TestProduct(unittest.TestCase):
    def setUp(self):
        Product.set_type_to_price({"A": 0, "B": 1})
        self.type_str = "A"
        self.product = Product(self.type_str)

    def test_set_type_to_price(self):
        new_type_to_price = {"C", 2}
        Product.set_type_to_price(new_type_to_price)
        self.assertEqual(Product.type_to_price, new_type_to_price)

    def test_get_type(self):
        self.assertEqual(self.product.get_type(), self.type_str.upper())

    def test_set_invalid_type(self):
        self.assertRaises(InvalidOptionError, self.product.set_type, "Blabla")
        self.assertEqual(self.product.type_, self.type_str.upper())

    def test_get_price(self):
        self.assertRaises(NotImplementedError, self.product.get_price)

    def test_edit(self):
        self.assertRaises(NotImplementedError, self.product.edit, {})


class TestDrink(unittest.TestCase):
    def setUp(self):
        Drink.set_type_to_price({"COKE": Decimal("2.00"),
                                 "JUICE": Decimal("3.01")})
        self.drink = Drink("Juice")

    def test_getprice(self):
        self.assertEqual(self.drink.get_price(), Decimal("3.01"))

    def test_edit_type(self):
        self.drink.edit({"type": "coke"})
        self.assertEqual(self.drink.get_type(), "COKE")

    def test_edit_invalid_options(self):
        self.assertRaises(InvalidOptionError, self.drink.edit, {1: "bla"})
        self.assertRaises(InvalidOptionError, self.drink.edit, {"type": 0})
        self.assertRaises(
            InvalidOptionError, self.drink.edit, {
                "type": "none"})


class TestPizza(unittest.TestCase):
    def setUp(self):
        Pizza.set_type_to_price({"PEPPERONI": Decimal("6.99"),
                                 "CUSTOM": Decimal("5.99")})
        Pizza.set_size_to_price({"SMALL": Decimal("0.00"),
                                 "MEDIUM": Decimal("2.00")})
        Pizza.set_topping_to_price({"OLIVE": Decimal("1.00"),
                                    "CHICKEN": Decimal("2.00"),
                                    "BEEF": Decimal("2.00"), })
        self.pizza = Pizza("Small", ["Beef", "Chicken"], "Custom")
        self.prev_toppings_len = 2

    def test_set_size_to_price(self):
        new_size_to_price = {"Mini", 2}
        Pizza.set_size_to_price(new_size_to_price)
        self.assertEqual(Pizza.size_to_price, new_size_to_price)

    def test_set_topping_to_price(self):
        new_topping_to_price = {"Spinach", 4}
        Pizza.set_topping_to_price(new_topping_to_price)
        self.assertEqual(Pizza.topping_to_price, new_topping_to_price)

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
                               "'Blabla' is not a valid topping option",
                               self.pizza.remove_topping,
                               "Blabla")
        self.assertEqual(len(self.pizza.toppings), self.prev_toppings_len)

    def test_get_price(self):
        self.assertEqual(self.pizza.get_price(), Decimal("9.99"))

    def test_edit_size(self):
        self.pizza.edit({"size": "Medium"})
        self.assertEqual(self.pizza.get_size(), "MEDIUM")

    def test_edit_type(self):
        self.pizza.edit({"type": "Pepperoni"})
        self.assertEqual(self.pizza.get_type(), "PEPPERONI")

    def test_edit_topping(self):
        self.pizza.edit({"toppings": ["Beef", "Chicken", "Olive"]})
        self.assertEqual(
            self.pizza.get_toppings(), [
                "BEEF", "CHICKEN", "OLIVE"])

    def test_edit_invalid_options(self):
        self.assertRaises(InvalidOptionError, self.pizza.edit, {1: "bla"})
        self.assertRaises(InvalidOptionError, self.pizza.edit, {"size": 1})
        self.assertRaises(InvalidOptionError, self.pizza.edit, {"type": 0})
        self.assertRaises(
            InvalidOptionError, self.pizza.edit, {
                "type": "mini"})
        self.assertRaises(
            InvalidOptionError, self.pizza.edit, {
                "toppings": "str"})
        self.assertRaises(
            InvalidOptionError, self.pizza.edit, {
                "toppings": [
                    "str", 1]})
        self.assertEqual(self.pizza.get_size(), "SMALL")
        self.assertEqual(self.pizza.get_type(), "CUSTOM")
        self.assertEqual(self.pizza.get_toppings(), ["BEEF", "CHICKEN"])


class TestCart(unittest.TestCase):
    def setUp(self):
        Drink.set_type_to_price({"COKE": Decimal("2.00"),
                                 "JUICE": Decimal("3.01")})
        self.cart = Cart()

    def test_initial_empty_cart(self):
        self.assertEqual(self.cart.products, {})
        self.assertEqual(self.cart.next_id, 1)

    def test_add_one_product(self):
        cart_item_id = self.cart.add_product(Drink("Juice"))
        self.assertEqual(self.cart.products[cart_item_id].get_type(), "JUICE")
        self.assertEqual(self.cart.next_id, 2)

    def test_valid_cart_item_id(self):
        self.assertFalse(self.cart.valid_cart_item_id(1))
        self.cart.add_product(Drink("Juice"))
        self.assertTrue(self.cart.valid_cart_item_id(1))
        self.cart.add_product(Drink("Coke"))
        self.assertFalse(self.cart.valid_cart_item_id(0))
        self.assertTrue(self.cart.valid_cart_item_id(1))
        self.assertTrue(self.cart.valid_cart_item_id(2))
        self.assertFalse(self.cart.valid_cart_item_id(3))

    def test_add_and_remove_product(self):
        cart_item_id = self.cart.add_product(Drink("Juice"))
        self.cart.remove_product(cart_item_id)
        self.assertEqual(self.cart.products, {})
        self.assertEqual(self.cart.next_id, 2)  # id's keep incrementing

    def test_edit_product(self):
        self.cart.add_product(Drink("Juice"))
        self.cart.edit_product(1, {"type": "Coke"})
        self.assertEqual(self.cart.products[1].get_type(), "COKE")

    def test_get_total_price(self):
        self.cart.add_product(Drink("Juice"))
        self.cart.add_product(Drink("Coke"))
        self.assertEqual(self.cart.get_total_price(), Decimal("5.01"))

    def test_get_products(self):
        self.cart.add_product(Drink("Juice"))
        self.cart.add_product(Drink("Coke"))
        products = self.cart.get_products()
        self.assertEqual(products[0][0], 1)  # Currently id indexing starts at 1
        self.assertEqual(products[0][1].get_type(), "JUICE")
        self.assertEqual(products[1][0], 2)
        self.assertEqual(products[1][1].get_type(), "COKE")


class TestOrder(unittest.TestCase):
    def setUp(self):
        Drink.set_type_to_price({"COKE": Decimal("2.00"),
                                 "JUICE": Decimal("3.01")})
        self.cart = Cart()
        self.cart.add_product(Drink("Juice"))
        self.cart.add_product(Drink("Coke"))
        self.order = Order(0, self.cart)

    def test_initialize_order(self):
        self.assertEqual(self.order.order_no, 0)
        self.assertIsInstance(self.order.delivery_method, Pickup)
        self.assertEqual(self.order.cart.get_products()[0][1].get_type(), "JUICE")
        self.assertEqual(self.order.cart.get_products()[1][1].get_type(), "COKE")
        self.assertEqual(len(self.order.cart.get_products()), 2)
        new_delivery_method = FoodoraDelivery("32 random")
        new_order = Order(3, self.cart, new_delivery_method)
        self.assertIsInstance(new_order.delivery_method, FoodoraDelivery)

    def test_get_order_no(self):
        self.assertEqual(self.order.get_order_no(), 0)

    def test_get_cart(self):
        self.assertEqual(self.order.get_cart().get_products()
                         [0][1].get_type(), "JUICE")
        self.assertEqual(self.order.get_cart().get_products()
                         [1][1].get_type(), "COKE")

    def test_get_delivery_method(self):
        self.assertIsInstance(self.order.get_delivery_method(), Pickup)

    def test_set_cart(self):
        new_cart = Cart()
        new_cart.add_product(Drink("Coke"))
        self.order.set_cart(new_cart)
        self.assertEqual(self.order.get_cart().get_products()
                         [0][1].get_type(), "COKE")
        self.assertEqual(len(self.order.get_cart().get_products()), 1)

    def test_set_delivery_method(self):
        new_delivery_method = Pickup()
        self.order.set_delivery_method(new_delivery_method)
        self.assertIsInstance(self.order.get_delivery_method(), Pickup)

    def test_checkout(self):
        self.assertEqual(self.order.checkout(), Decimal("5.01"))


class TestDeliveryMethod(unittest.TestCase):
    def setUp(self):
        self.delivery_method = DeliveryMethod()

    def test_deliver(self):
        self.assertRaises(NotImplementedError, self.delivery_method.deliver)


class TestPickUp(unittest.TestCase):
    def setUp(self):
        self.pickup = Pickup()

    def test_deliver(self):
        self.assertEqual(
            self.pickup.deliver(),
            "Your order is ready for pickup!")


class TestPizzeriaDelivery(unittest.TestCase):
    def setUp(self):
        self.delivery = PizzeriaDelivery("Dundas")

    def test_initialize(self):
        self.assertEqual(self.delivery.address, "Dundas")

    def test_set_address(self):
        self.delivery.set_address("St. George")
        self.assertEqual(self.delivery.address, "St. George")

    def test_deliver(self):
        self.assertEqual(
            self.delivery.deliver(),
            "Your delivery is on its way!")


class TestUberEatsDelivery(unittest.TestCase):
    def setUp(self):
        self.delivery = UberEatsDelivery("Dundas")

    def test_initialize(self):
        self.assertEqual(self.delivery.address, "Dundas")

    def test_set_address(self):
        self.delivery.set_address("St. George")
        self.assertEqual(self.delivery.address, "St. George")

    def test_deliver(self):
        self.assertEqual(
            self.delivery.deliver(),
            "Your Uber Eats delivery is on its way!")


class TestFoodoraDelivery(unittest.TestCase):
    def setUp(self):
        self.delivery = FoodoraDelivery("Dundas")

    def test_initialize(self):
        self.assertEqual(self.delivery.address, "Dundas")

    def test_set_address(self):
        self.delivery.set_address("St. George")
        self.assertEqual(self.delivery.address, "St. George")

    def test_deliver(self):
        self.assertEqual(
            self.delivery.deliver(),
            "Your Foodora delivery is on its way!")


class TestOrderParser(unittest.TestCase):
    def setUp(self):
        self.order_parser = OrderParser()

    def test_get_product_list(self):
        self.assertRaises(
            NotImplementedError,
            self.order_parser.get_product_list,
            None)

    def test_get_address(self):
        self.assertRaises(
            NotImplementedError,
            self.order_parser.get_address,
            None)

    def test_get_order_no(self):
        self.assertRaises(
            NotImplementedError,
            self.order_parser.get_order_no,
            None)


class TestJsonParser(unittest.TestCase):
    def setUp(self):
        self.json = sample_json
        self.parser = JsonParser()
        setup_options()

    def test_get_product_list(self):
        self.assertIsInstance(
            self.parser.get_product_list(
                self.json)[0], Pizza)
        self.assertEqual(
            self.parser.get_product_list(
                self.json)[0].get_price(),
            Decimal("8.99"))
        self.assertIsInstance(
            self.parser.get_product_list(
                self.json)[1], Drink)
        self.assertEqual(
            self.parser.get_product_list(
                self.json)[1].get_price(),
            Decimal("2.00"))

    def test_get_address(self):
        self.assertEqual(
            self.parser.get_address(
                self.json),
            "74 random street")

    def test_get_order_no(self):
        self.assertEqual(self.parser.get_order_no(self.json), 1)

    def test_get_json(self):
        new_json = self.parser.get_json(
            [(1, Pizza("small", ["Pepperoni"], "Custom")), (3, Drink("Water"))])
        self.assertEqual(new_json["products"][0]["cart_item_id"], 1)
        self.assertEqual(new_json["products"][0]["product_category"], "pizza")
        self.assertEqual(new_json["products"][0]["size"], "SMALL")
        self.assertEqual(new_json["products"][0]["type"], "CUSTOM")
        self.assertEqual(new_json["products"][0]["toppings"], ["PEPPERONI"])


class TestCsvParser(unittest.TestCase):
    def setUp(self):
        self.csv_string = 'drink,coke_zero,\npizza,custom,small,\npizza,pepperoni,extra_large,olive\nfoodora,27 random street,2'
        self.parser = CsvParser()
        setup_options()

    def test_get_product_list(self):
        self.assertIsInstance(
            self.parser.get_product_list(
                self.csv_string)[0], Drink)
        self.assertEqual(
            self.parser.get_product_list(
                self.csv_string)[0].get_type(),
            "COKE_ZERO")
        self.assertIsInstance(
            self.parser.get_product_list(
                self.csv_string)[1], Pizza)
        self.assertEqual(
            self.parser.get_product_list(
                self.csv_string)[1].get_type(),
            "CUSTOM")
        self.assertEqual(
            self.parser.get_product_list(
                self.csv_string)[1].get_size(),
            "SMALL")
        self.assertEqual(
            self.parser.get_product_list(
                self.csv_string)[1].get_toppings(),
            [])

    def test_get_address(self):
        self.assertEqual(
            self.parser.get_address(
                self.csv_string),
            "27 random street")

    def test_get_order_no(self):
        self.assertEqual(self.parser.get_order_no(self.csv_string), 2)

