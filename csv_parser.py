from order_parser import OrderParser
from order import Order
from product import Product
from typing import Any, List, Dict
from pizza import Pizza
from drink import Drink
import csv


class CsvParser(OrderParser):
    """A class to parse csv object into internal data structures."""

    def __init__(self, csv: Dict[str, Any]):
        """Initialize a csv parser. """
        self.set_csv(csv)

    def set_json(self, csv):
        """Set this csv parsers csv to csv"""
        self.csv = csv

    def get_product_list(self) -> List[Product]:
        """Return the list of products in this order."""
        list_products = []
        split_lines = self.csv.split("\n")
        for line in split_lines:
            split_line = line.split(",")
            if split_line[0] == "pizza":
                pizza = Pizza(split_line[1], split_line[3:], split_line[2])
                list_products.append(pizza)
            elif split_line[1] == "drink":
                drink = Drink(split_line[2])
                list_products.append(drink)
        return list_products

    def get_address(self) -> str:
        """Return the address of this order."""
        #TODO