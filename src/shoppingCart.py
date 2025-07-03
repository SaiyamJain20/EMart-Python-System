import uuid
from src.product import Product

class ShoppingCart:
    """
    Represents a shopping cart containing multiple products.
    """

    def __init__(self, customer_id: str):
        """
        Initializes a new shopping cart.
        """
        self.cart_id = uuid.uuid4().hex
        self.customer_id = customer_id
        self.items = []  # List of tuples (Product, quantity)

    def add_item(self, product: Product, qty: int) -> bool:
        """
        Adds an item to the cart.
        """
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if product.product_stock < qty:
            raise ValueError(f"Not enough stock available for {product.product_name}.")

        for idx, (p, q) in enumerate(self.items):
            if p.product_id == product.product_id:
                new_qty = q + qty
                if product.product_stock < new_qty:
                    raise ValueError(f"Only {product.product_stock} available for {product.product_name}.")
                self.items[idx] = (p, new_qty)
                product.update_stock(-qty)  # Reduce stock
                return True

        self.items.append((product, qty))
        product.update_stock(-qty)  # Reduce stock
        return True

    def remove_item(self, product: Product) -> bool:
        """
        Removes an item from the cart.
        """
        for p, q in self.items:
            if p.product_id == product.product_id:
                product.update_stock(q)  # Restore stock before removing item
                break

        self.items = [(p, q) for (p, q) in self.items if p.product_id != product.product_id]
        return True

    def calculate_total(self, customer_type: str) -> float:
        """
        Calculates the total cost of items in the cart.
        """
        return sum(product.get_price(customer_type) * qty for product, qty in self.items)

    def view_cart(self) -> str:
        """
        Displays the contents of the cart.
        """
        if not self.items:
            return "Cart is empty."
        
        cart_details = "\n".join(
            f"{product.product_name} (x{qty}) - ${product.get_price('individual') * qty:.2f}"
            for product, qty in self.items
        )
        return f"Shopping Cart:\n{cart_details}\nTotal: ${self.calculate_total('individual'):.2f}"

    def clear_cart(self) -> bool:
        """
        Clears the cart of all items.
        """
        self.items = []
        return True