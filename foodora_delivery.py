from delivery_method import DeliveryMethod


class FoodoraDelivery(DeliveryMethod):
    """A Foodora delivery method.

    address: Address to send delivery.
    """
    def __init__(self, address: str, order_no: int) -> None:
        """Initialize a new Foodora delivery."""
        self.set_address(address)
        self.set_order_no(order_no)

    def set_address(self, address: str) -> None:
        """Set the address of Foodora delivery."""
        self.address = address

    def set_order_no(self, order_no: int):
        """Set the order number of this delivery method. """
        self.order_no = order_no

    def deliver(self) -> None:
        """Inform customer that their Foodora delivery is on its way."""
        return "Your Foodora delivery is on its way!"