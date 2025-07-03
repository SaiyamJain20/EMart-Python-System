from src.product import Product

class Inventory:
    """
    Manages inventory for a specific product in the E-Mart system.

    Attributes:
        product_id (str): Unique identifier for the associated product.
        inventory_quantity (int): Current stock quantity of the product.
    """

    def __init__(self, product: Product, quantity: int):
        """
        Initializes an Inventory instance.
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.product_id = product.product_id  # Associated product's ID
        self.inventory_quantity = quantity 

    def check_availability(self) -> int:
        """
        Checks the available stock quantity.
        """
        return self.inventory_quantity

    def update_quantity(self, qty: int) -> bool:
        """
        Updates the inventory quantity.
        """
        if self.inventory_quantity + qty < 0:
            raise ValueError("Inventory quantity cannot go negative.")
        self.inventory_quantity += qty 
        return True
