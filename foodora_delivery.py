from delivery_method import DeliveryMethod


class FoodoraDelivery(DeliveryMethod):
    """A Foodora delivery method.

    address: Address to send delivery.
    """
    def __init__(self, address: str) -> None:
        """Initialize a new Foodora delivery."""
        self.set_address(address)

    def set_address(self, address: str) -> None:
        """Set the address of Foodora delivery."""
        self.address = address

    def deliver(self) -> None:
        """Inform customer that their Foodora delivery is on its way."""
        return "Your Foodora delivery is on its way!"