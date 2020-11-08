from decimal import Decimal

from cart import Cart
from delivery_method import DeliveryMethod


class Order:
    """Represents a order placed in the pizzeria system.

    order_no: the order number of this order.
    cart: the cart of items in this order
    delivery_method: the method to deliver this order.
    """

    def __init__(self, order_no: int, cart: Cart) -> None:
        self.order_no = order_no
        self.cart = cart
        self.delivery_method = None

    def set_delivery_method(self, delivery_method: DeliveryMethod) -> None:
        self.delivery_method = delivery_method

    def checkout(self) -> Decimal:
        """Checkout this order."""
        if self.delivery_method is not None:
            # Not in-store pickup
            self.delivery_method.deliver()
        return self.cart.get_total_price()
