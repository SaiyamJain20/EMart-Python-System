# E-Mart System Overview

## System Components

- Product Management: Handles product details, inventory management, and product categorization
- User Management: Supports customer registration, authentication, and profile management with different customer types (Individual and Retail)
- Shopping Experience: Implements shopping cart functionality, product search, and checkout process
- Order Processing: Manages orders, delivery tracking, and status updates
- Discount System: Supports coupons with validation and expiry date checks
Key Classes
- EMarketSystem: Central system managing all components and their interactions
- Customer/User: User authentication and profile management
- Product/Inventory: Product information and stock management
- ShoppingCart: Handles product selection before checkout
- Order/Delivery: Order processing and delivery tracking
- Coupon: Discount management with validity checks
- Category: Product categorization for better organization

## Workflows

- Registration & Login: User account creation and authentication
- Shopping: Product browsing, searching, and cart management
- Checkout: Order placement with optional coupon application
- Order Tracking: Monitoring delivery status of placed orders
- Admin Features: Coupon generation and delivery status management

# How to run

## To run src

```
python3 -m src.main
```

## To run testcases

```
pytest testcases -s -v
```

# E-Mart System Test Cases

### User Registration & Authentication
1. **Successful registration**: Verifies a new customer can be registered with valid details.
2. **Duplicate username rejection**: Tests that system prevents registering users with identical usernames.
3. **Duplicate email rejection**: Ensures the system prevents multiple accounts with the same email address.
4. **Invalid email format validation**: Confirms the system rejects registration with improperly formatted emails.
5. **Successful login**: Tests that a registered user can successfully authenticate with correct credentials.
6. **Password verification**: Verifies login is rejected when incorrect password is provided.
7. **Non-existent user handling**: Tests system properly handles login attempts with unknown usernames.
8. **Empty field validation**: Confirms system rejects registration with any empty required fields.
9. **Phone number validation**: Tests that phone numbers must be 10 digits and numeric.

### Product Management
10. **Product creation and categorization**: Verifies products can be added and assigned to categories.
11. **Negative price validation**: Ensures the system rejects products with negative prices.
12. **Negative stock validation**: Tests that products cannot be created with negative stock quantities.
13. **Zero price validation**: Confirms products with zero prices are rejected.

### Shopping Cart
14. **Adding items to cart**: Verifies products can be added to a customer's shopping cart.
15. **Stock availability check**: Tests that adding items exceeding available stock is prevented.
16. **Quantity validation**: Ensures quantities added to cart must be positive numbers.
17. **Non-existent product handling**: Verifies system handles attempts to add nonexistent products to cart.
18. **Non-existent user handling**: Tests system properly handles cart operations for invalid user IDs.

### Order Processing
19. **Empty cart validation**: Confirms checkout is prevented when cart contains no items.
20. **Coupon application**: Tests that valid coupons correctly apply discounts during checkout.
21. **Non-existent coupon handling**: Verifies system properly handles checkout with invalid coupon codes.
22. **Expired coupon validation**: Tests that expired coupons are rejected during checkout.
23. **Stock reduction after checkout**: Confirms product inventory is reduced after successful order placement.
24. **Inventory consistency between orders**: Verifies that stock depletion prevents subsequent orders for same product.

### Delivery Management
25. **Status update verification**: Tests that delivery status can be updated after order placement.
26. **Non-existent order handling**: Verifies system properly handles tracking requests for nonexistent orders.

### Search Functionality
27. **Product search by name**: Tests that products can be found by partial name matches.
28. **Product search by category**: Verifies that products can be retrieved by their assigned category.