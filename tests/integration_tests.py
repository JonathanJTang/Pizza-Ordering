import json
import unittest
from unittest.mock import patch
from decimal import Decimal

import options
from cart import Cart
from drink import Drink
from invalid_option_error import InvalidOptionError
from pizza import Pizza
from PizzaParlour import app
from product import Product


# JSON data sample for In house delivery
sample_json = {
    "data_format": "json_tree",
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


with open("order_schema_json.json") as schema:
    order_schema_json_tree = json.load(open("order_schema_json.json"))

class TestIntegration(unittest.TestCase):
    def setUp(self):
        Drink.set_type_to_price(options.DRINK_TYPE_TO_PRICE)
        Pizza.set_type_to_price(options.PIZZA_TYPE_TO_PRICE)
        Pizza.set_size_to_price(options.PIZZA_SIZE_TO_PRICE)
        Pizza.set_topping_to_price(options.PIZZA_TOPPING_TO_PRICE)

        app.testing = True
        self.app = app.test_client()

    def test_request(self):
        response = self.app.get("/pizza")
        self.assertEqual(response.status_code, 200)

    # def test_create_order(self):
    #     unittest.mock.create_autospec()

    # @patch('PizzaParlour.order_schema_json_tree', order_schema_json_tree)
    def test_add_order(self):
        response = self.app.post("/api/orders")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'1')
        response = self.app.get(
            "/api/orders/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'{"products":[]}\n')
        response = self.app.put(
            "/api/orders/1",
            json=sample_json)
        self.assertEqual(response.data, b'{"total_price":10.99}\n')
        response.get_json()
