from delivery_method import DeliveryMethod


class PizzeriaDelivery(DeliveryMethod):
    """A pizzeria delivery method.
    
    address: Address to send delivery.
    """

    def __init__(self, address: str) -> None:
        """Initialize a new pizzeria delivery."""
        self.set_address(address)

    def set_address(self, address: str) -> None:
        """Set the address of pizzeria delivery."""
        self.address = address

    def deliver(self) -> None:
        """Inform customer that their delivery is on its way."""
        return "Your delivery is on its way!"
