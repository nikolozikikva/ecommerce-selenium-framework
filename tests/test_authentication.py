"""Authentication test cases covering valid, locked out, invalid, and performance edge cases."""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import (
    STANDARD_USER,
    LOCKED_OUT_USER,
    PERFORMANCE_GLITCH_USER,
    PASSWORD,
    INVENTORY_URL,
)


class TestAuthentication:
    """Test suite for authentication workflows and error handling."""

    def test_valid_login(self, driver):
        """Verify standard user can successfully log in and access inventory."""
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(STANDARD_USER, PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded(), "Inventory page should be visible after valid login"
        assert INVENTORY_URL in driver.current_url, (
            f"Expected URL to contain '{INVENTORY_URL}', got '{driver.current_url}'"
        )

    def test_locked_out_user(self, driver):
        """Verify locked-out user receives the appropriate error banner."""
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(LOCKED_OUT_USER, PASSWORD)

        assert login_page.is_error_displayed(), "Error banner should be displayed for locked-out user"
        error_text = login_page.get_error_message()
        assert "Sorry, this user has been locked out." in error_text, (
            f"Unexpected error message: '{error_text}'"
        )

    def test_invalid_credentials(self, driver):
        """Verify attempting to log in with invalid credentials triggers an error banner."""
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login("invalid_user_name", "wrong_password")

        assert login_page.is_error_displayed(), "Error banner should be displayed for invalid credentials"
        error_text = login_page.get_error_message()
        assert "Username and password do not match any user in this service" in error_text, (
            f"Unexpected error message: '{error_text}'"
        )

    def test_performance_glitch_user_login(self, driver):
        """Verify performance glitch user completes login smoothly via explicit waits."""
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(PERFORMANCE_GLITCH_USER, PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded(), (
            "Inventory page should load reliably despite performance glitch delay"
        )
        assert INVENTORY_URL in driver.current_url, (
            f"Expected URL to contain '{INVENTORY_URL}', got '{driver.current_url}'"
        )
