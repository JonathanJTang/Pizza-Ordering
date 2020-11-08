from delivery_method import DeliveryMethod


class Pickup(DeliveryMethod):
    """A pickup delivery method."""

    def deliver(self) -> None:
        """Inform customer that their pickup is ready."""
        return "Your order is ready for pickup!"