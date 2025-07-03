class Search:
    """
    Handles searching for products by name and category.
    """

    def __init__(self, products: list, categories: list):
        """
        Initializes the search system.
        """
        self.products = products or []  # Ensure it's always a list
        self.categories = categories or []

    def search_by_name(self, name: str) -> list:
        """
        Searches for products by name.
        """
        name = name.strip().lower()
        return [p for p in self.products if name in p.product_name.lower()]

    def search_by_category(self, cat: str) -> list:
        """
        Searches for products in a specific category.
        """
        cat = cat.strip().lower()
        for category in self.categories:
            if cat == category.category_name.lower():
                return category.get_products()
        return []
