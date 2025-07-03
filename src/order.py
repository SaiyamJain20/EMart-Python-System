import uuid

class Order:
    """
    Represents an order placed by a customer in the E-Mart system.

    Attributes:
        order_id (str): Unique identifier for the order.
        customer_id (str): Identifier for the customer placing the order.
        order_items (list): List of (product, quantity) tuples.
        order_total_amount (float): Total price of the order after applying discounts.
        order_status (str): Current status of the order (e.g., Pending, Placed, Cancelled).
        order_coupon (Coupon or None): Applied coupon for the order.
    """

    def __init__(self, customer_id: str, items: list):
        """
        Initializes an Order instance.
        """
        if not items:
            raise ValueError("Order must contain at least one item.")
        
        self.order_id = uuid.uuid4().hex    # Generate a unique order ID
        self.customer_id = customer_id      # Store the customer's ID
        self.order_items = items            # List of (Product, quantity) tuples
        self.order_total_amount = 0.0       
        self.order_status = "Pending"       
        self.order_coupon = None            

    def place_order(self, customer_type: str) -> bool:
        """
        Places the order and calculates the total amount.
        """
        if not self.order_items:
            raise ValueError("Order is empty.")
        
        # Calculate total order amount based on product prices and quantities
        self.order_total_amount = sum(
            product.get_price(customer_type) * qty
            for product, qty in self.order_items
        )

        # Apply coupon discount if available
        if self.order_coupon:
            discount_amount = self.order_total_amount * (self.order_coupon.coupon_discount / 100)
            self.order_total_amount -= discount_amount
        
        self.order_status = "Placed" 
        return True

    def cancel_order(self) -> bool:
        """
        Cancels the order.
        """
        self.order_status = "Cancelled"
        return True

    def get_order_status(self) -> str:
        """
        Retrieves the current order status.
        """
        return self.order_status

    def apply_coupon(self, coupon) -> float:
        """
        Applies a coupon discount to the order.
        """
        if coupon and coupon.is_valid():
            self.order_coupon = coupon  # Assign the coupon to the order
            discount_amount = self.order_total_amount * (coupon.coupon_discount / 100)
            self.order_total_amount -= discount_amount
        
        return self.order_total_amount
