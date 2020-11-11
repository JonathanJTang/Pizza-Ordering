from order_parser import OrderParser
from order import Order
from product import Product
from typing import Any, List, Dict
from pizza import Pizza
from drink import Drink


class JsonParser(OrderParser):
    """A class to parse JSON object into internal data structures."""

    def __init__(self, json: Dict[str, Any]):
        """Initialize a JSON parser. """
        self.set_json(json)

    def set_json(self, json):
        """Set this JSON parsers JSON to json"""
        self.json = json

    def get_product_list(self) -> List[Product]:
        """Return the list of products in this order."""
        list_products = []
        product_dictionaries_list = self.json["products"]
        for product in product_dictionaries_list:
            if product["product_category"] == "pizza":
                pizza = Pizza(product["size"], product["toppings"], product["type"])
                list_products.append(pizza)
            elif product["product_category"] == "drink":
                drink = Drink(product["type"])
                list_products.append(drink)
        return list_products

    def get_address(self) -> str:
        """Return the address of this order."""
        #TODO