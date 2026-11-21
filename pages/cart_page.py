"""Page Object for SauceDemo Shopping Cart Page."""

from typing import List
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Encapsulates locators and interactions for the Cart Page."""

    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def is_loaded(self) -> bool:
        """Verify the cart page has loaded."""
        return self.is_displayed(self.CHECKOUT_BUTTON)

    def get_item_names(self) -> List[str]:
        """Return list of item names present in the cart."""
        if not self.is_displayed(self.ITEM_NAME, timeout=3):
            return []
        elements = self.find_all_visible(self.ITEM_NAME)
        return [el.text.strip() for el in elements]

    def get_item_prices(self) -> List[float]:
        """Return list of item prices present in the cart as floats."""
        if not self.is_displayed(self.ITEM_PRICE, timeout=3):
            return []
        elements = self.find_all_visible(self.ITEM_PRICE)
        return [float(el.text.replace("$", "").strip()) for el in elements]

    def remove_item_by_name(self, product_name: str) -> None:
        """Remove a product from the cart by its name."""
        xpath = (
            f"//div[contains(@class, 'cart_item')]"
            f"[.//div[contains(@class, 'inventory_item_name') and text()='{product_name}']]"
            f"//button[text()='Remove']"
        )
        self.click((By.XPATH, xpath))

    def click_checkout(self) -> None:
        """Click the Checkout button to begin checkout."""
        self.click(self.CHECKOUT_BUTTON)
