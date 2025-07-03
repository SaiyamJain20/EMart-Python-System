from src.user import User
from src.helperFunctions import is_valid_email

class Customer(User):
    """
    Represents a customer in the E-Mart system. Inherits from User.

    Attributes:
        customer_name (str): The full name of the customer.
        customer_email (str): The email of the customer.
        customer_address (str): The residential address of the customer.
        customer_phone (str): The contact number of the customer.
        customer_loyalty_points (int): Points earned through purchases.
        customer_coupons (list): A list of available discount coupons.
    """

    def __init__(self, username: str, password: str, email: str,
                 name: str, address: str, phone: str):
        """
        Initializes a customer with the necessary details.
        """
        super().__init__(username, password, email)
        
        if not name or not address or not phone:
            raise ValueError("All fields are required.")

        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Invalid phone number.")

        self.customer_name = name
        self.customer_email = email
        self.customer_address = address
        self.customer_phone = phone
        self.customer_loyalty_points = 0  # Default loyalty points
        self.customer_coupons = []  # List of available coupons

    def register(self) -> bool:
        """
        Registers the customer in the system.
        """
        return True  # Placeholder for actual registration logic

    def update_profile(self, name: str, address: str, phone: str, email: str) -> bool:
        """
        Updates the customer's profile details.
        """
        if email and not is_valid_email(email):
            raise ValueError("Invalid email format.")

        self.customer_name = name if name else self.customer_name
        self.customer_address = address if address else self.customer_address
        self.customer_phone = phone if phone else self.customer_phone
        self.customer_email = email if email else self.customer_email

        return True

    def get_available_coupons(self) -> list:
        """
        Retrieves the list of available discount coupons for the customer.
        """
        return self.customer_coupons

class IndividualCustomer(Customer):
    """
    Represents an individual customer in the E-Mart system.
    Inherits from Customer and applies retail pricing.
    """

    def __init__(self, username: str, password: str, email: str,
                 name: str, address: str, phone: str):
        """
        Initializes an individual customer.
        """
        super().__init__(username, password, email, name, address, phone)

    def get_retail_price(self, product) -> float:
        """
        Retrieves the retail price of a product for the customer.
        """
        return product.product_retail_price

class RetailCustomer(Customer):
    """
    Represents a retail customer (business) in the E-Mart system.
    Inherits from Customer and applies wholesale pricing.
    """

    def __init__(self, username: str, password: str, email: str,
                 name: str, address: str, phone: str, business_license: str):
        """
        Initializes a retail customer with business-specific details.
        """
        super().__init__(username, password, email, name, address, phone)
        if not business_license:
            raise ValueError("Business license is required for retail customers.")
        self.customer_business_license = business_license  # Store business license

    def get_wholesale_price(self, product) -> float:
        """
        Retrieves the wholesale price of a product for the retail customer.
        """
        return product.product_wholesale_price
