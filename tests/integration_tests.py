import json
import unittest
from unittest.mock import patch

import cli
import options
from click.testing import CliRunner
from drink import Drink
from pizza import Pizza
from PizzaParlour import app


base_order = {
    "products": [],
    "delivery_method": {
        "type": "pickup",
        "details": {}
    }
}

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

    @patch("cli.requests.delete")
    @patch("cli.requests.put")
    @patch("cli.requests.post")
    def test_workflow(self, mock_post, mock_put, mock_delete):
        """Works when Flask server is already running."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(cli.menu)
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(cli.menu, args=["coke"])
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(cli.order)
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(
            cli.order, args=["new"], obj={"current_order": base_order})
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(
            cli.order,
            args=["pizza", "small", "custom", "-t", "olive"],
            obj={"current_order": base_order})
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(cli.order, args=["drink", "coke"],
                               obj={"current_order": base_order})
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(cli.order, args=["edit"],
                               obj={"current_order": base_order},
                               input="0\n")
        self.assertTrue(result.exit_code == 0 and not result.exception)

        mock_post.return_value.status_code = 200
        mock_post.return_value.text = "1"
        mock_put.return_value.status_code = 200
        mock_put.return_value.json = lambda: {"total_price": "6.78"}
        result = runner.invoke(cli.order, args=["submit"],
                               obj={"current_order": base_order},
                               input="foodora\n27 random street\n")
        self.assertTrue(result.exit_code == 0 and not result.exception)
        self.assertIn("Your order has been successfully submitted. " +
                      "The total price is " +
                      "$6.78, and your order number is 1", result.output)

        mock_delete.return_value.status_code = 200
        result = runner.invoke(cli.order, args=["cancel", "1"])
        self.assertTrue(result.exit_code == 0 and not result.exception)
        self.assertIn("Successfully cancelled order 1", result.output)

    @patch("cli.requests.patch")
    @patch("cli.requests.get")
    def test_edit_previous_order(self, mock_get, mock_patch):
        input_str = "1\nedit\nsize\nlarge\n1\nedit\ntype\npepperoni\n2\nedit\npepsi\n2\ndelete\n1\nedit\nadd_topping\nolive\n1\nedit\nremove_topping\nbacon\n0\n"
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: {"products": [
            {
                'cart_item_id': 1,
                'product_category': 'pizza',
                'size': 'small',
                'toppings': ['bacon'],
                'type': 'custom'},
            {
                'cart_item_id': 2,
                'product_category': 'drink',
                'type': 'coke'}]}
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.text = "12.34"
        result = CliRunner().invoke(cli.order, args=["edit", "1"],
                                    obj={"current_order": base_order},
                                    input=input_str)
        self.assertTrue(result.exit_code == 0 and not result.exception)
        self.assertIn("The price of the new order is $12.34", result.output)
