from typing import Any, List

from order import Order


class OrderParser:
    """Object to parse received data to create an order."""

    def get_product_list(self, csv_or_json) -> List[Order]:
        """Return the list of products in this order."""
        raise NotImplementedError()

    def get_address(self, csv_or_json) -> str:
        """Return the address of this order."""
        raise NotImplementedError()

    def get_order_no(self, csv_or_json) -> int:
        """Return the order number of this order."""
        raise NotImplementedError()
