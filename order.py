from decimal import Decimal

from cart import Cart
from delivery_method import DeliveryMethod
from pickup import Pickup


class Order:
    """Represents a order placed in the pizzeria system.

    order_no: the order number of this order.
    cart: the cart of items in this order
    delivery_method: the method to deliver this order.
    """

    def __init__(self, order_no: int, cart: Cart) -> None:
        self.order_no = order_no
        self.cart = cart
        self.delivery_method = Pickup()  # default to in-store pickup

    def get_order_no(self) -> int:
        """Getter for order number."""
        return self.order_no

    def get_cart(self) -> Cart:
        """Getter for cart."""
        return self.cart

    def get_delivery_method(self) -> DeliveryMethod:
        """Getter for delivery method."""
        return self.delivery_method

    def set_cart(self, cart: Cart) -> None:
        """Setter for cart."""
        self.cart = cart

    def set_delivery_method(self, delivery_method: DeliveryMethod) -> None:
        """Setter for delivery method."""
        self.delivery_method = delivery_method

    def checkout(self) -> Decimal:
        """Checkout this order."""
        self.delivery_method.deliver()
        return self.cart.get_total_price()
