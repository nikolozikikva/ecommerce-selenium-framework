"""End-to-end checkout workflow and checkout form validation tests."""

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.config import STANDARD_USER, PASSWORD


class TestCheckoutE2E:
    """Test suite for full checkout lifecycle and edge cases."""

    def test_complete_e2e_purchase_flow(self, driver):
        """Complete purchase flow: login -> add 2 items -> cart -> checkout -> verify math -> finish."""
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(STANDARD_USER, PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()

        product_1 = "Sauce Labs Backpack"
        product_2 = "Sauce Labs Bike Light"

        inventory_page.add_item_to_cart(product_1)
        inventory_page.add_item_to_cart(product_2)
        assert inventory_page.get_cart_badge_count() == 2

        inventory_page.open_cart()

        cart_page = CartPage(driver)
        assert cart_page.is_loaded(), "Cart page should be loaded"
        cart_items = cart_page.get_item_names()
        assert product_1 in cart_items, f"'{product_1}' should be in cart"
        assert product_2 in cart_items, f"'{product_2}' should be in cart"

        cart_page.click_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_customer_info(
            first_name="John",
            last_name="Tester",
            postal_code="94043",
        )
        checkout_page.click_continue()

        # Step Two Overview: Verify financial calculations
        actual_subtotal = checkout_page.get_subtotal()
        expected_subtotal = 39.98
        assert actual_subtotal == expected_subtotal, (
            f"Expected item subtotal {expected_subtotal}, got {actual_subtotal}"
        )

        expected_tax = round(expected_subtotal * 0.08, 2)
        actual_tax = checkout_page.get_tax()
        assert actual_tax == expected_tax, (
            f"Expected 8% tax calculation {expected_tax}, got {actual_tax}"
        )

        expected_total = round(expected_subtotal + expected_tax, 2)
        actual_total = checkout_page.get_total()
        assert actual_total == expected_total, (
            f"Expected grand total {expected_total}, got {actual_total}"
        )

        # Step Three: Complete order
        checkout_page.click_finish()
        assert checkout_page.is_order_completed(), "Order confirmation header should be displayed"
        confirmation_text = checkout_page.get_complete_header()
        assert confirmation_text == "Thank you for your order!", (
            f"Unexpected confirmation header: '{confirmation_text}'"
        )

    def test_checkout_negative_missing_postal_code(self, driver):
        """Negative test: submitting checkout step one without postal code shows inline error."""
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(STANDARD_USER, PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()
        inventory_page.add_item_to_cart("Sauce Labs Backpack")
        inventory_page.open_cart()

        cart_page = CartPage(driver)
        assert cart_page.is_loaded()
        cart_page.click_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_customer_info(
            first_name="John",
            last_name="Tester",
            postal_code="",
        )
        checkout_page.click_continue()

        assert checkout_page.is_error_displayed(), (
            "Error banner should appear when postal code is missing"
        )
        error_message = checkout_page.get_error_message()
        assert "Error: Postal Code is required" in error_message, (
            f"Unexpected validation message: '{error_message}'"
        )
