from order_parser import OrderParser
from product import Product
from typing import List
from pizza import Pizza
from drink import Drink


class CsvParser(OrderParser):
    """A class to parse csv object into internal data structures."""

    def get_product_list(self, csv) -> List[Product]:
        """Return the list of products in this order."""
        list_products = []
        split_lines = csv.split("\n")
        for line in split_lines:
            split_line = line.split(",")
            if split_line[0] == "pizza":
                pizza = Pizza(split_line[2], split_line[3].split("|"), split_line[1]) #TODO test for no toppings.
                list_products.append(pizza)
            elif split_line[1] == "drink":
                drink = Drink(split_line[1])
                list_products.append(drink)
        return list_products

    def get_address(self, csv) -> str:
        """Return the address of this order."""
        split_lines = csv.split("\n")
        delivery_line = split_lines[-1]
        return delivery_line[1]
        
    def get_order_no(self, csv) -> int:
        """Return the order number of this order."""
        split_lines = csv.split("\n")
        delivery_line = split_lines[-1]
        return delivery_line[2]