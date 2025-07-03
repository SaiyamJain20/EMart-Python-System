from src.customer import Customer, RetailCustomer
from src.product import Product
from src.category import Category
from src.order import Order
from src.delivery import Delivery
from src.coupon import Coupon
from src.search import Search
from src.shoppingCart import ShoppingCart

class EMarketSystem:
    """
    Represents an e-commerce marketplace system.
    Manages customers, products, orders, shopping carts, coupons, and deliveries.
    """

    def __init__(self):
        """Initializes the e-market system with empty collections for managing users, products, and orders."""
        self.customers = {}       # Maps user_id to Customer objects
        self.usernames = {}       # Maps username to user_id
        self.products = {}        # Maps product_id to Product objects
        self.categories = {}      # Maps category_id to Category objects
        self.orders = {}          # Maps order_id to Order objects
        self.deliveries = {}      # Maps order_id to Delivery objects
        self.coupons = {}         # Maps coupon code to Coupon objects
        self.shopping_carts = {}  # Maps customer_id to ShoppingCart objects

    def register_customer(self, customer: Customer) -> Customer:
        """
        Registers a new customer in the system.
        """
        if customer.username in self.usernames:
            raise ValueError("Username already exists. Please choose another username.")
        for cust in self.customers.values():
            if cust.customer_email.lower() == customer.email.lower():
                raise ValueError("Email already registered. Please use another email.")

        # Store customer details
        self.customers[customer.user_id] = customer
        self.usernames[customer.username] = customer.user_id

        # Create a shopping cart for the new customer
        self.shopping_carts[customer.user_id] = ShoppingCart(customer.user_id)
        return customer

    def login_customer(self, username: str, password: str) -> Customer:
        """
        Authenticates a customer by username and password.
        """
        if username in self.usernames:
            user_id = self.usernames[username]
            customer = self.customers[user_id]
            if customer.login(password):
                return customer
            else:
                raise ValueError("Incorrect password.")
        raise ValueError("Username not found. Please register first.")

    def add_product(self, product: Product, category_name: str) -> Product:
        """
        Adds a product to the system under a specified category.
        """
        self.products[product.product_id] = product
        cat = None

        # Find or create the category
        for category in self.categories.values():
            if category.category_name.lower() == category_name.lower():
                cat = category
                break
        if not cat:
            cat = Category(category_name)
            self.categories[cat.category_id] = cat

        # Associate product with category
        cat.add_product(product)
        return product

    def add_coupon(self, coupon: Coupon) -> Coupon:
        """
        Adds a discount coupon to the system.
        """
        self.coupons[coupon.coupon_code] = coupon
        return coupon

    def add_to_cart(self, customer_id: str, product_id: str, quantity: int) -> bool:
        """
        Adds a product to the customer's shopping cart.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if customer_id not in self.shopping_carts:
            raise ValueError("No shopping cart found for this customer.")
        if product_id not in self.products:
            raise ValueError("Product not found.")

        product = self.products[product_id]
        if product.product_stock < quantity:
            raise ValueError("Insufficient stock.")

        # Add product to cart without reducing stock immediately
        self.shopping_carts[customer_id].add_item(product, quantity)
        return True

    def checkout_order(self, customer_id: str, coupon_code: str = None) -> Order:
        """
        Processes the checkout for a customer, creating an order and handling coupons.
        """
        if customer_id not in self.shopping_carts:
            raise ValueError("Shopping cart not found for this customer.")

        cart = self.shopping_carts[customer_id]
        if not cart.items:
            raise ValueError("Shopping cart is empty.")

        # Get customer type for pricing
        customer = self.customers[customer_id]
        customer_type = "retail" if isinstance(customer, RetailCustomer) else "individual"

        # Validate stock before finalizing order
        for product, qty in cart.items:
            if product.product_stock < -qty:
                raise ValueError(f"Insufficient stock for {product.product_name}.")

        # Create and place the order
        order = Order(customer_id, cart.items)
        if coupon_code:
            if coupon_code in self.coupons:
                if not self.coupons[coupon_code].is_valid():
                    raise ValueError("Coupon has expired.")
                order.order_coupon = self.coupons[coupon_code]
            else:
                raise ValueError("Coupon not found.")

        order.place_order(customer_type)
        self.orders[order.order_id] = order

        # Initiate delivery for the order
        delivery = Delivery(order.order_id)
        self.deliveries[order.order_id] = delivery

        # Reset the cart after checkout
        self.shopping_carts[customer_id] = ShoppingCart(customer_id)
        return order

    def search_products(self, name: str) -> list:
        """
        Searches for products by name.
        """
        search_engine = Search(list(self.products.values()), list(self.categories.values()))
        return search_engine.search_by_name(name)

    def search_category(self, category_name: str) -> list:
        """
        Searches for products within a specific category.
        """
        search_engine = Search(list(self.products.values()), list(self.categories.values()))
        return search_engine.search_by_category(category_name)

    def track_delivery(self, order_id: str) -> Delivery:
        """
        Tracks the delivery status of an order.
        """
        return self.deliveries.get(order_id, None)
