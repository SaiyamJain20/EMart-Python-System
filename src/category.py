import uuid
from src.product import Product

class Category:
    """
    Represents a category in the E-Mart system.

    Attributes:
        category_id (str): A unique identifier for the category.
        category_name (str): The name of the category.
        category_products (list): A list to store products belonging to this category.
    """
    def __init__(self, name: str):
        """
        Initializes a new category with a unique ID and name.
        """
        if not name:
            raise ValueError("Category name is required.")
        self.category_id = uuid.uuid4().hex     # Generate a unique category ID
        self.category_name = name
        self.category_products = []                      # List to hold products in this category

    def get_products(self) -> list:
        """
        Retrieves the list of products in this category.
        """
        return self.category_products

    def add_product(self, product: Product) -> bool:
        """
        Adds a product to this category.
        """
        self.category_products.append(product)
        return True
