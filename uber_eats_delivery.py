from delivery_method import DeliveryMethod


class UberEatsDelivery(DeliveryMethod):
    """A Uber Eats delivery method.

    address: Address to send delivery.
    """
    def __init__(self, address: str, order_no: int) -> None:
        """Initialize a new Uber Eats delivery."""
        self.set_address(address)
        self.set_order_no(order_no)

    def set_address(self, address: str) -> None:
        """Set the address of Uber Eats delivery."""
        self.address = address

    def set_order_no(self, order_no: int):
        """Set the order number of this delivery method. """
        self.order_no = order_no

    def deliver(self) -> None:
        """Inform customer that their Uber Eats delivery is on its way."""
        return "Your Uber Eats delivery is on its way!"