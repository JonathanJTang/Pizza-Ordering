from delivery_method import DeliveryMethod


class UberEatsDelivery(DeliveryMethod):
    """A Uber Eats delivery method.

    address: Address to send delivery.
    """
    def __init__(self, address: str) -> None:
        """Initialize a new Uber Eats delivery."""
        self.set_address(address)

    def set_address(self, address: str) -> None:
        """Set the address of Uber Eats delivery."""
        self.address = address

    def deliver(self) -> None:
        """Inform customer that their Uber Eats delivery is on its way."""
        return "Your Uber Eats delivery is on its way!"