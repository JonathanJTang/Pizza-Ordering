import unittest

import cli
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

    def test_no_crash(self):
        """Works when Flask server is already running."""
        runner = CliRunner()
        result = runner.invoke(cli.menu)
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(cli.menu, args=["item"])
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
        result = runner.invoke(cli.order, args=["edit", "1"],
                               obj={"current_order": base_order},
                               input="0\n")
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(cli.order, args=["submit"],
                               obj={"current_order": base_order},
                               input="pickup\n")
        self.assertTrue(result.exit_code == 0 and not result.exception)
        result = runner.invoke(cli.order, args=["cancel", "1"])
        self.assertTrue(result.exit_code == 0 and not result.exception)
