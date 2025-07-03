import uuid

class Product:
    """
    Represents a product in the E-Mart system.

    Attributes:
        product_id (str): Unique identifier for the product.
        product_name (str): Name of the product.
        product_description (str): Description of the product.
        product_retail_price (float): Retail price per unit.
        product_wholesale_price (float): Wholesale price per unit.
        product_stock (int): Number of units available in stock.
        product_discount_percent (int): Percentage discount applied (0-100%).
    """

    def __init__(self, name: str, description: str, retail_price: float, wholesale_price: float, stock: int):
        """
        Initializes a Product instance.
        """
        if not name:
            raise ValueError("Product name is required.")
        if retail_price == 0 or wholesale_price == 0:
            raise ValueError("Prices cannot be zero.")
        if retail_price < 0 or wholesale_price < 0:
            raise ValueError("Prices cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")

        self.product_id = uuid.uuid4().hex  # Generate a unique product ID
        self.product_name = name
        self.product_description = description
        self.product_retail_price = retail_price
        self.product_wholesale_price = wholesale_price
        self.product_stock = stock
        self.product_discount_percent = 0  # Default: No discount

    def get_details(self) -> str:
        """
        Returns a formatted string containing product details.
        """
        return (
            f"ID: {self.product_id}\n"
            f"Name: {self.product_name}\n"
            f"Description: {self.product_description}\n"
            f"Retail Price: ${self.product_retail_price:.2f}\n"
            f"Wholesale Price: ${self.product_wholesale_price:.2f}\n"
            f"Stock: {self.product_stock}\n"
            f"Discount: {self.product_discount_percent}%"
        )

    def update_stock(self, qty: int) -> bool:
        """
        Updates the stock quantity.
        """
        if self.product_stock + qty < 0:
            raise ValueError("Stock cannot go negative.")
        
        self.product_stock += qty
        return True

    def set_discount(self, pct: int) -> None:
        """
        Sets a discount percentage on the product.
        """
        if not (0 <= pct <= 100):
            raise ValueError("Discount percentage must be between 0 and 100.")
        
        self.product_discount_percent = pct

    def get_price(self, customer_type: str) -> float:
        """
        Returns the price after applying any discount.
        """
        base_price = self.product_wholesale_price if customer_type == "retail" else self.product_retail_price
        return round(base_price * (1 - self.product_discount_percent / 100), 2)
