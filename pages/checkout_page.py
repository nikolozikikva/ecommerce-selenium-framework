"""Page Object for SauceDemo Checkout Flows (Step One, Step Two, Complete)."""

import re
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


def _parse_currency(text: str) -> float:
    """Helper to extract float currency amount from string (e.g., 'Item total: $39.98' -> 39.98)."""
    match = re.search(r"\$([\d,]+\.?\d*)", text)
    if match:
        return float(match.group(1).replace(",", ""))
    raise ValueError(f"Could not parse numeric price from text: '{text}'")


class CheckoutPage(BasePage):
    """Encapsulates locators and interactions across the checkout flow."""

    # Step One Locators
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")

    # Step Two (Overview) Locators
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")

    # Step Three (Complete) Locators
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def fill_customer_info(
        self, first_name: str = "", last_name: str = "", postal_code: str = ""
    ) -> None:
        """Fill in checkout customer details in Step One."""
        self.type_text(self.FIRST_NAME_INPUT, first_name, clear_first=True)
        self.type_text(self.LAST_NAME_INPUT, last_name, clear_first=True)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code, clear_first=True)

    def click_continue(self) -> None:
        """Click Continue button on checkout step one."""
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        """Retrieve the inline error message on Step One."""
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self, timeout: int = 3) -> bool:
        """Check if an error banner is displayed on Step One."""
        return self.is_displayed(self.ERROR_CONTAINER, timeout=timeout)

    def get_subtotal(self) -> float:
        """Extract and parse the item subtotal from Step Two overview."""
        text = self.get_text(self.SUBTOTAL_LABEL)
        return _parse_currency(text)

    def get_tax(self) -> float:
        """Extract and parse the tax amount from Step Two overview."""
        text = self.get_text(self.TAX_LABEL)
        return _parse_currency(text)

    def get_total(self) -> float:
        """Extract and parse the grand total from Step Two overview."""
        text = self.get_text(self.TOTAL_LABEL)
        return _parse_currency(text)

    def click_finish(self) -> None:
        """Click Finish button on Step Two to place order."""
        self.click(self.FINISH_BUTTON)

    def get_complete_header(self) -> str:
        """Return the completion header text on Order Confirmation."""
        return self.get_text(self.COMPLETE_HEADER)

    def is_order_completed(self) -> bool:
        """Verify the order completion header is displayed."""
        return self.is_displayed(self.COMPLETE_HEADER)
