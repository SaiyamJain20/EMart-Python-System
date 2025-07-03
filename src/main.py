import json
import datetime
from src.EMarketSystem import EMarketSystem
from src.customer import Customer, IndividualCustomer, RetailCustomer
from src.coupon import Coupon
from src.product import Product
from src.helperFunctions import is_valid_email, input_non_empty, input_int, input_float

def addBaseProducts(system: EMarketSystem, filename="./src/products.json"):
    """
    Loads product data from a JSON file and adds them to the system.
    """
    try:
        with open(filename, "r") as file:
            products = json.load(file)  # Load JSON file
        
        for item in products:
            try:
                # Create a Product instance
                product = Product(item["name"], item["description"], item["price"], item["cost"], item["stock"])
                system.add_product(product, item["category"])
            except ValueError as ve:
                print(f"Error adding product {item['name']}: {ve}")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error loading product file:", e)

def addAdminUser(system: EMarketSystem):
    """
    Registers the admin user into the system with predefined credentials.
    """
    try:
        admin = Customer("admin", "admin", "admin@dollmart.com", "Admin", "HQ", "0000000000")
        system.register_customer(admin)
    except ValueError as ve:
        print("Error registering admin:", ve)

def main():
    """
    Entry point for the E-Market System. Handles user registration, login, 
    product searches, cart operations, checkout, order tracking, and admin functions.
    """
    system = EMarketSystem()
    addBaseProducts(system)
    addAdminUser(system)
    
    current_user = None  # Holds the logged-in user
    
    while True:
        if not current_user:
            # User authentication menu
            print("\n=== Dollmart E-Market System ===")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                # Register a new customer
                print("\n=== Register Customer ===")
                while True:
                    try:
                        username = input_non_empty("Username: ")
                        password = input_non_empty("Password: ")
                        email = input_non_empty("Email: ")
                        if not is_valid_email(email):
                            print("Invalid email format. Please try again.")
                            continue
                        name = input_non_empty("Full Name: ")
                        address = input_non_empty("Address: ")
                        phone = input_non_empty("Phone: ")
                        cust_type = input_non_empty("Customer Type (individual/retail): ").lower()

                        if cust_type not in ["individual", "retail"]:
                            print("Invalid customer type. Please enter 'individual' or 'retail'.")
                            continue

                        # Create customer instance based on type
                        if cust_type == "individual":
                            customer = IndividualCustomer(username, password, email, name, address, phone)
                        else:
                            business_license = input_non_empty("Business License Number: ")
                            customer = RetailCustomer(username, password, email, name, address, phone, business_license)

                        system.register_customer(customer)
                        print("Registration successful! You can now log in.")
                        break

                    except ValueError as ve:
                        print("Registration error:", ve)
                        print("Please try again.")

            elif choice == "2":
                # Login process
                print("\n=== Login ===")
                try:
                    username = input_non_empty("Username: ")
                    password = input_non_empty("Password: ")
                    user = system.login_customer(username, password)
                    current_user = user
                    print(f"Welcome, {current_user.customer_name}!")
                except ValueError as ve:
                    print("Login error:", ve)

            elif choice == "3":
                print("Exiting system. Goodbye!")
                break

            else:
                print("Invalid choice. Try again.")

        else:
            # Dashboard menu for logged-in users
            print(f"\n=== Dashboard ({current_user.username}) ===")
            print("1. Search Product by Name")
            print("2. Search Product by Category")
            print("3. Add Product to Cart")
            print("4. View Shopping Cart")
            print("5. Checkout Order")
            print("6. Track Delivery")
            print("7. Update Profile")
            
            if current_user.username == "admin":
                print("8. Generate Coupon")
                print("9. Update Delivery Status")
                print("10. Logout")
            else:
                print("8. Logout")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                # Product search by name
                query = input_non_empty("Enter product name to search: ")
                results = system.search_products(query)
                if results:
                    print("\n--- Search Results ---")
                    for p in results:
                        print(p.get_details())
                        print("-" * 40)
                else:
                    print("No products found.")

            elif choice == "2":
                # Product search by category
                print("\n--- Available Categories ---")
                if not system.categories:
                    print("No categories available.")
                else:
                    for cat_obj in system.categories.values():
                        print(f"- {cat_obj.category_name}")

                    chosen_cat = input_non_empty("Enter the category name to explore: ")
                    results = system.search_category(chosen_cat)
                    if results:
                        print(f"\n--- Products in '{chosen_cat}' ---")
                        for p in results:
                            print(p.get_details())
                            print("-" * 40)
                    else:
                        print(f"No products found in '{chosen_cat}'.")

            elif choice == "3":
                # Add product to cart
                print("\n--- Available Products ---")
                for p in system.products.values():
                    print(p.get_details())
                    print("-" * 40)

                prod_id = input_non_empty("Enter Product ID to add to cart: ")
                try:
                    qty = input_int("Enter quantity: ", 1)
                    system.add_to_cart(current_user.user_id, prod_id, qty)
                    print("Product added to cart.")
                except Exception as e:
                    print("Error adding product to cart:", e)

            elif choice == "4":
                # View shopping cart
                cart = system.shopping_carts[current_user.user_id]
                print("\n--- Your Shopping Cart ---")
                print(cart.view_cart())

            elif choice == "5":
                # Checkout process
                coupon_code = input("Enter coupon code (press Enter to skip): ").strip() or None
                try:
                    order = system.checkout_order(current_user.user_id, coupon_code)
                    print("\nOrder placed successfully!")
                    print(f"Order ID: {order.order_id}")
                    print(f"Total Amount: ${order.order_total_amount:.2f}")
                except Exception as e:
                    print("Checkout error:", e)
                    
            elif choice == "6":
                # Track delivery
                order_id = input_non_empty("Enter Order ID to track delivery: ")
                delivery = system.track_delivery(order_id)
                if delivery:
                    print(f"Delivery Status: {delivery.track_delivery()}")
                    print(f"Estimated Delivery Time: {delivery.get_estimated_time()}")
                else:
                    print("Order not found or no delivery info available.")

            elif choice == "7":
                # Update profile
                print("\n--- Update Profile ---")
                new_name = input("New name (press Enter to skip): ").strip()
                new_address = input("New address (press Enter to skip): ").strip()
                new_phone = input("New phone (press Enter to skip): ").strip()
                new_email = input("New email (press Enter to skip): ").strip()
                try:
                    current_user.update_profile(new_name, new_address, new_phone, new_email)
                    print("Profile updated.")
                except ValueError as ve:
                    print("Profile update error:", ve)

            elif choice == "8" and current_user.username != "admin":
                # Logout for regular customers
                current_user = None
                print("Logged out successfully.")
            
            elif choice == "8" and current_user.username == "admin":
                # Generate coupon
                print("\n--- Generate Coupon ---")
                code = input_non_empty("Enter coupon code: ")
                discount = input_float("Enter discount percentage: ", 0, 100)
                expiry_str = input_non_empty("Enter expiry date (YYYY-MM-DD): ")
                try:
                    expiry_date = datetime.datetime.strptime(expiry_str, "%Y-%m-%d").date()
                    coupon = Coupon(code, discount, expiry_date)
                    system.add_coupon(coupon)
                    print("Coupon generated successfully.")
                except Exception as e:
                    print("Error generating coupon:", e)

            elif choice == "9" and current_user.username == "admin":
                # Update delivery status
                print("\n--- Update Delivery Status ---")
                order_id = input_non_empty("Enter Order ID to update: ")
                if order_id in system.deliveries:
                    new_status = input_non_empty("Enter new delivery status: ")
                    try:
                        system.deliveries[order_id].update_status(new_status)
                        print("Delivery status updated.")
                    except ValueError as ve:
                        print("Error updating delivery status:", ve)
                else:
                    print("Order not found.")
                    
            elif choice == "10" and current_user.username == "admin":
                # Logout for admin
                current_user = None
                print("Logged out successfully.")

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
