class AbstractProduct:
    """An abstract class for products in the pizzeria system."""
    def get_price(self):
        """Return the price of this product. This is an abstract method."""
        raise NotImplementedError()
