import unittest
from unittest.mock import patch

import cli
import click
from click.testing import CliRunner

base_order = {
    "products": [],
    "delivery_method": {
        "type": "pickup",
        "details": {}
    }
}

order_data = {
    "data_format": "csv",
    "products": [
        {
            "product_category": "drink",
            "type": "coke_zero"
        },
        {
            "product_category": "pizza",
            "size": "small",
            "type": "custom",
            "toppings": []
        },
        {
            "product_category": "pizza",
            "size": "extra_large",
            "type": "pepperoni",
            "toppings": ["olive", "beef"]
        },

    ],
    "delivery_method": {
        "type": "foodora",
        "details": {
            "address": "27 random street",
            "order_no": 2
        }
    }
}


class TestCliUtilityFunctions(unittest.TestCase):
    def test_convert_to_csv(self):
        expected = "drink,coke_zero,\npizza,custom,small,\npizza,pepperoni,extra_large,olive|beef\nfoodora,27 random street,2"
        actual = cli.convert_to_csv(order_data)
        self.assertEqual(actual, expected)


class TestCli(unittest.TestCase):
    def setUp(self):
        pass

    @patch("cli.requests.get")
    def test_valid_full_menu(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = lambda: {
            "Part A": {"Item 1": 1.00, "Item 2": 1.99}}
        runner = CliRunner()
        result = runner.invoke(cli.menu)
        self.assertTrue(result.exit_code == 0 and not result.exception)
        self.assertEqual(
            result.output,
            "Part A:\nItem 1       :  $1.0\nItem 2       :  $1.99\n\n")

    @patch("cli.requests.get")
    def test_valid_menu_item(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "1.00"
        result = CliRunner().invoke(cli.menu, args=["random_item"])
        self.assertTrue(result.exit_code == 0 and not result.exception)
        self.assertEqual(result.output, "random_item: $1.00\n")

    @patch("cli.requests.get")
    def test_invalid_menu_item(self, mock_get):
        mock_get.return_value.status_code = 400
        mock_get.return_value.text = "Error text"
        result = CliRunner().invoke(cli.menu, args=["random_item"])
        self.assertTrue(result.exit_code == 0 and not result.exception)
        self.assertEqual(
            result.output,
            "Error: random_item is not a valid menu item\n")

    def test_add_pizza_and_drink(self):
        expected = {"products": [{
                "product_category": "pizza",
                "size": "small",
                "type": "custom",
                "toppings": [
                    "olive",
                ]
            },
            {
                "product_category": "drink",
                "type": "coke",
            },
        ],
            "delivery_method": {
                "type": "pickup",
                "details": {}
            }
        }
        context = {"current_order": base_order}
        result = CliRunner().invoke(
            cli.order,
            args=["pizza", "small", "custom", "-t", "olive"],
            obj=context)
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = CliRunner().invoke(
            cli.order,
            args=["drink", "coke"],
            obj=context)
        self.assertTrue(result.exit_code == 0 and not result.exception)
        self.assertEqual(context["current_order"], expected)
