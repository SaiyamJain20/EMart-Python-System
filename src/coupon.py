import uuid
import datetime

class Coupon:
    """
    Represents a discount coupon in the E-Mart system.

    Attributes:
        coupon_id (str): A unique identifier for the coupon.
        coupon_code (str): The coupon code used for applying discounts.
        coupon_discount (float): The discount percentage (0 to 100).
        coupon_expiry_date (datetime.date): The date when the coupon expires.
    """

    def __init__(self, code: str, discount: float, expiry_date: datetime.date):
        """
        Initializes a new coupon with a unique ID, code, discount, and expiry date.
        """
        if not code:
            raise ValueError("Coupon code is required.")
        if discount < 0 or discount > 100:
            raise ValueError("Discount must be between 0 and 100.") 

        self.coupon_id = uuid.uuid4().hex  # Generate a unique coupon ID
        self.coupon_code = code  # Coupon code
        self.coupon_discount = discount  # Discount percentage
        self.coupon_expiry_date = expiry_date  # Expiration date

    def apply_discount(self, amount: float) -> float:
        """
        Applies the discount to the given amount.
        """
        discount_amount = amount * (self.coupon_discount / 100)
        return amount - discount_amount

    def is_valid(self) -> bool:
        """
        Checks if the coupon is still valid based on the expiry date.
        """
        return datetime.date.today() <= self.coupon_expiry_date
