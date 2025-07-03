import pytest
import datetime
from time import sleep
from src.EMarketSystem import EMarketSystem
from src.customer import Customer, IndividualCustomer
from src.product import Product
from src.coupon import Coupon

@pytest.fixture
def system():
    """
    Creates a fresh EMarketSystem instance for each test.
    """
    return EMarketSystem()

# 1) ---------------------------
def test_register_customer_success(system):
    cust = Customer("u1", "passA", "u1@example.com", "UserOne", "A1", "1111111111")
    system.register_customer(cust)
    assert cust.user_id in system.customers
    assert system.customers[cust.user_id].username == "u1"

# 2) ---------------------------
def test_register_customer_existing_username(system):
    cust1 = Customer("user", "passA", "one@example.com", "One", "A1", "1234567890")
    cust2 = Customer("user", "passB", "two@example.com", "Two", "A2", "4567890123")
    system.register_customer(cust1)
    with pytest.raises(ValueError) as exc:
        system.register_customer(cust2)
    assert "Username already exists" in str(exc.value)

# 3) ---------------------------
def test_register_customer_existing_email(system):
    cust1 = Customer("u1", "passA", "duplicate@example.com", "One", "A1", "1234567890")
    cust2 = Customer("u2", "passB", "duplicate@example.com", "Two", "A2", "4567890123")
    system.register_customer(cust1)
    with pytest.raises(ValueError) as exc:
        system.register_customer(cust2)
    assert "Email already registered" in str(exc.value)

# 4) ---------------------------
def test_register_customer_invalid_email(system):
    with pytest.raises(ValueError) as exc:
        Customer("u1", "passA", "invalid-email", "One", "A1", "9999999999")
    assert "Invalid email format" in str(exc.value)

# 5) ---------------------------
def test_login_customer_success(system):
    cust = Customer("u1", "passA", "login1@example.com", "Login User", "A1", "9999999999")
    system.register_customer(cust)
    logged_in = system.login_customer("u1", "passA")
    assert logged_in == cust

# 6) ---------------------------
def test_login_customer_incorrect_password(system):
    cust = Customer("u1", "passA", "login2@example.com", "User", "A1", "9999999999")
    system.register_customer(cust)
    with pytest.raises(ValueError) as exc:
        system.login_customer("u1", "passB")
    assert "Incorrect password" in str(exc.value)

# 7) ---------------------------
def test_login_customer_nonexistent_username(system):
    with pytest.raises(ValueError) as exc:
        system.login_customer("no_such_user", "passA")
    assert "Username not found" in str(exc.value)
    
# 8) --------------------------
def test_register_customer_empty_fields(system):
    with pytest.raises(ValueError) as exc:
        Customer("", "password", "email@example.com", "Name", "Address", "1234567890")
    assert "All fields are required." in str(exc.value)

    with pytest.raises(ValueError) as exc:
        Customer("user", "", "email@example.com", "Name", "Address", "1234567890")
    assert "All fields are required." in str(exc.value)

    with pytest.raises(ValueError) as exc:
        Customer("user", "password", "", "Name", "Address", "1234567890")
    assert "All fields are required." in str(exc.value)

# 9) --------------------------
def test_register_customer_invalid_phone_number(system):
    with pytest.raises(ValueError) as exc:
        Customer("userX", "passX", "valid@example.com", "NameX", "AddrX", "12345")  # Too short
    assert "Invalid phone number" in str(exc.value)

    with pytest.raises(ValueError) as exc:
        Customer("userY", "passY", "valid@example.com", "NameY", "AddrY", "abcdefghij")  # Not digits
    assert "Invalid phone number" in str(exc.value)

# 10) ---------------------------
def test_add_product_success(system):
    prod = Product("TestProduct", "Description", 10.0, 8.0, 5)
    system.add_product(prod, "TestCategory")
    assert prod.product_id in system.products
    # Check category created
    assert any(cat.category_name.lower() == "testcategory" for cat in system.categories.values())

# 11) ---------------------------
def test_add_product_negative_price(system):
    # Negative retail price should raise an error
    with pytest.raises(ValueError) as exc:
        Product("BadProd", "Desc", -5.0, 3.0, 10)
    assert "Prices cannot be negative" in str(exc.value)

# 12) --------------------------
def test_add_product_negative_stock(system):
    with pytest.raises(ValueError) as exc:
        Product("BadStock", "Desc", 5.0, 4.0, -1)
    assert "Stock cannot be negative" in str(exc.value)

# 13) --------------------------
def test_add_product_zero_price(system):
    with pytest.raises(ValueError) as exc:
        Product("ZeroPriceProd", "Description", 0.0, 0.0, 5)
    assert "Prices cannot be zero." in str(exc.value)
    
# 14) --------------------------
def test_add_to_cart_success(system):
    cust = IndividualCustomer("cartuser", "cartpass", "cart@example.com", "CartUser", "Addr", "9999999999")
    prod = Product("CartProd", "Desc", 10.0, 9.0, 10)
    system.register_customer(cust)
    system.add_product(prod, "Misc")
    # Add to cart
    system.add_to_cart(cust.user_id, prod.product_id, 2)
    cart = system.shopping_carts[cust.user_id]
    assert len(cart.items) == 1
    assert cart.items[0][1] == 2  # quantity

# 15) --------------------------
def test_add_to_cart_insufficient_stock(system):
    cust = IndividualCustomer("stockuser", "stockpass", "stock@example.com", "StockUser", "Addr", "9999999999")
    prod = Product("LowStock", "Desc", 10.0, 9.0, 1)
    system.register_customer(cust)
    system.add_product(prod, "Misc")
    with pytest.raises(ValueError) as exc:
        system.add_to_cart(cust.user_id, prod.product_id, 5)
    assert "Insufficient stock" in str(exc.value)

# 16) --------------------------
def test_add_to_cart_invalid_quantity(system):
    cust = IndividualCustomer("qtyuser", "qtypass", "qty@example.com", "QtyUser", "Addr", "9999999999")
    prod = Product("QtyProd", "Desc", 10.0, 8.0, 10)
    system.register_customer(cust)
    system.add_product(prod, "Misc")
    with pytest.raises(ValueError) as exc:
        system.add_to_cart(cust.user_id, prod.product_id, 0)  # zero quantity
    assert "Quantity must be greater than zero" in str(exc.value)

# 17) --------------------------
def test_add_to_cart_nonexistent_product(system):
    cust = IndividualCustomer("cartuserX", "cartpassX", "cartX@example.com", "CartUserX", "AddrX", "7777777777")
    system.register_customer(cust)
    with pytest.raises(ValueError) as exc:
        system.add_to_cart(cust.user_id, "nonexistent_product", 1)
    assert "Product not found" in str(exc.value)

# 18) --------------------------
def test_add_to_cart_nonexistent_user(system):
    prod = Product("SomeProduct", "Desc", 15.0, 12.0, 10)
    system.add_product(prod, "Misc")
    with pytest.raises(ValueError) as exc:
        system.add_to_cart("nonexistent_user", prod.product_id, 2)
    assert "No shopping cart found for this customer." in str(exc.value)
    
# 19) --------------------------
def test_checkout_order_empty_cart(system):
    cust = IndividualCustomer("emptycart", "emptypass", "empty@example.com", "Empty Cart", "Addr", "9999999999")
    system.register_customer(cust)
    with pytest.raises(ValueError) as exc:
        system.checkout_order(cust.user_id)
    assert "Shopping cart is empty" in str(exc.value)

# 20) --------------------------
def test_checkout_order_with_coupon(system):
    cust = IndividualCustomer("couponuser", "couponpass", "coupon@example.com", "Coupon User", "Addr", "9999999999")
    prod = Product("Laptop", "Desc", 1000.0, 900.0, 5)
    # Add a valid coupon
    expiry = datetime.date.today() + datetime.timedelta(days=5)
    coupon = Coupon("SAVE10", 10, expiry)
    system.register_customer(cust)
    system.add_product(prod, "Electronics")
    system.add_to_cart(cust.user_id, prod.product_id, 1)
    system.add_coupon(coupon)
    # Checkout
    order = system.checkout_order(cust.user_id, coupon_code="SAVE10")
    assert order.order_status == "Placed"
    # 1000 minus 10% = 900 if no discount conflict
    assert pytest.approx(order.order_total_amount, 0.01) == 900.0

# 21) --------------------------
def test_checkout_order_coupon_not_found(system):
    cust = IndividualCustomer("badcoupon", "pass", "badcoupon@example.com", "Bad Coupon", "Addr", "9999999999")
    prod = Product("Phone", "Desc", 500.0, 450.0, 2)
    system.register_customer(cust)
    system.add_product(prod, "Electronics")
    system.add_to_cart(cust.user_id, prod.product_id, 1)
    with pytest.raises(ValueError) as exc:
        system.checkout_order(cust.user_id, coupon_code="NOTEXIST")
    assert "Coupon not found" in str(exc.value)

# 22) --------------------------
def test_checkout_invalid_coupon_expired(system):
    cust = IndividualCustomer("expCouponUser", "expPass", "exp@example.com", "ExpCoupon User", "Addr", "8888888888")
    prod = Product("Headphones", "Desc", 150.0, 120.0, 5)
    system.register_customer(cust)
    system.add_product(prod, "Electronics")
    system.add_to_cart(cust.user_id, prod.product_id, 1)

    # Expired coupon
    expired_date = datetime.date.today() - datetime.timedelta(days=1)
    coupon = Coupon("OLD50", 50, expired_date)
    system.add_coupon(coupon)

    with pytest.raises(ValueError) as exc:
        system.checkout_order(cust.user_id, coupon_code="OLD50")
    assert "Coupon has expired." in str(exc.value)

# 23) --------------------------
def test_checkout_stock_reduction(system):
    cust = IndividualCustomer("stockCheck", "stockPass", "stock@example.com", "Stock Checker", "Addr", "1010101010")
    prod = Product("LimitedStock", "Desc", 50.0, 40.0, 2)
    system.register_customer(cust)
    system.add_product(prod, "Electronics")

    system.add_to_cart(cust.user_id, prod.product_id, 2)
    system.checkout_order(cust.user_id)

    # Stock should be reduced to zero after purchase
    assert system.products[prod.product_id].product_stock == 0

# 24) --------------------------
def test_checkout_exceeding_stock_after_order(system):
    cust1 = IndividualCustomer("stockuser1", "pass1", "stock1@example.com", "StockUser1", "Addr1", "1111111111")
    cust2 = IndividualCustomer("stockuser2", "pass2", "stock2@example.com", "StockUser2", "Addr2", "2222222222")
    
    system.register_customer(cust1)
    system.register_customer(cust2)

    prod = Product("HotItem", "Desc", 30.0, 25.0, 1)  # Only 1 in stock
    system.add_product(prod, "Trending")

    system.add_to_cart(cust1.user_id, prod.product_id, 1)
    system.checkout_order(cust1.user_id)  # First user buys it

    with pytest.raises(ValueError) as exc:
        system.add_to_cart(cust2.user_id, prod.product_id, 1)  # Second user tries to buy
    assert "Insufficient stock" in str(exc.value)
    

# 25) --------------------------
def test_delivery_update_status(system):
    # Place an order, then update the delivery status
    cust = IndividualCustomer("deluser", "delpass", "del@example.com", "Del User", "Addr", "9999999999")
    prod = Product("Book", "Desc", 20.0, 15.0, 2)
    system.register_customer(cust)
    system.add_product(prod, "Books")
    system.add_to_cart(cust.user_id, prod.product_id, 1)
    order = system.checkout_order(cust.user_id)
    delivery = system.track_delivery(order.order_id)
    assert delivery is not None
    assert delivery.delivery_status == "Preparing"
    delivery.update_status("Shipped")
    assert delivery.delivery_status == "Shipped"

# 26) --------------------------
def test_delivery_track_nonexistent(system):
    delivery = system.track_delivery("nonexistent_order_id")
    assert delivery is None

# 27) --------------------------
def test_search_products_found(system):
    # Add some products
    p1 = Product("Banana", "Fruit", 1.0, 0.8, 50)
    p2 = Product("Bandana", "Accessory", 5.0, 4.0, 10)
    p3 = Product("Laptop", "Electronics", 1000, 900, 2)
    system.add_product(p1, "Grocery")
    system.add_product(p2, "Fashion")
    system.add_product(p3, "Electronics")

    results = system.search_products("Ban")
    # Should find Banana and Bandana
    names = [p.product_name for p in results]
    assert "Banana" in names
    assert "Bandana" in names
    assert "Laptop" not in names

# 28) --------------------------
def test_search_category_found(system):
    p1 = Product("Milk", "Dairy", 2.0, 1.8, 20)
    p2 = Product("Cheese", "Dairy product", 3.0, 2.5, 10)
    system.add_product(p1, "Grocery")
    system.add_product(p2, "Grocery")
    results = system.search_category("Grocery")
    assert len(results) == 2
    assert any(prod.product_name == "Milk" for prod in results)
    assert any(prod.product_name == "Cheese" for prod in results)


