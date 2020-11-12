from typing import Any, Dict, List, Tuple

from drink import Drink
from order_parser import OrderParser
from pizza import Pizza
from product import Product


class JsonParser(OrderParser):
    """A class to parse JSON object into internal data structures."""

    def get_product_list(self, json) -> List[Product]:
        """Return the list of products in this order."""
        list_products = []
        product_dictionaries_list = json["products"]
        for product in product_dictionaries_list:
            if product["product_category"] == "pizza":
                pizza = Pizza(
                    product["size"],
                    product["toppings"],
                    product["type"])
                list_products.append(pizza)
            elif product["product_category"] == "drink":
                drink = Drink(product["type"])
                list_products.append(drink)
        return list_products

    def get_json(self, product_list: List[Tuple[int, Product]]) \
                    -> Tuple[int, Dict[str, Any]]:
        """Return a dictionary to be jsonified from product list."""
        json = {"products": []}
        for cart_item_id, product in product_list:
            product_dictionary = {}
            product_dictionary["cart_item_id"] = cart_item_id
            if isinstance(product, Pizza):
                product_dictionary["product_category"] = "pizza"
                product_dictionary["size"] = product.get_size().upper()
                product_dictionary["type"] = product.get_type().upper()
                product_dictionary["toppings"] = product.get_toppings()
            elif isinstance(product, Drink):
                product_dictionary["product_category"] = "drink"
                product_dictionary["type"] = product.get_type()
            json["products"].append(product_dictionary)
        return json

    def get_address(self, json) -> str:
        """Return the address of this order."""
        return json["delivery_method"]["details"]["address"]

    def get_order_no(self, json) -> int:
        """Return the order number of this order."""
        return json["delivery_method"]["details"]["order_no"]
