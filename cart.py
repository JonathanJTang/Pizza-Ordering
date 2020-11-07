from typing import Dict, List, Union
from decimal import Decimal
from product import Product


class Cart:
    """A cart with Products.

    products: List of Products in the cart.
    """

    def __init__(self) -> None:
        """Initialize a new empty Cart."""
        self.products = {}
        self.next_id = 1  # This always increments, regardless of removed items

    def valid_cart_item_id(self, cart_item_id) -> bool:
        return cart_item_id in self.products.keys()

    def add_product(self, product: Product) -> int:
        """Add a new Product to Cart and return its id in the cart."""
        cart_item_id = self.next_id
        self.products[cart_item_id] = product
        self.next_id += 1
        return cart_item_id

    def remove_product(self, cart_item_id) -> Product:
        """Remove the product from Cart (and return it)."""
        if self.valid_cart_item_id(cart_item_id):
            return self.products.pop(cart_item_id)

    def edit_product(self, cart_item_id: int,
                     changes: Dict[str, Union[str, List[str]]]) -> None:
        """Edit the product with given id in the cart by applying given changes.
        If the id is not valid, or any of the changes are not valid, the
        appropriate error is raised."""
        if self.valid_cart_item_id(cart_item_id):
            self.products[cart_item_id].edit(changes)
        
    def get_total_price(self) -> Decimal:
        """Return the total price of all items in the Cart"""
        total = Decimal("0.00")
        for product in self.products.values():
            total += product.get_price()
        return total

    def get_products(self) -> List[Product]:
        """Return a list of Products in the Cart."""
        product_list = []
        for key in sorted(self.products.keys()):
            product_list.append(self.products[key])
        return product_list
