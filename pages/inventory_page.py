"""Page Object for SauceDemo Inventory Page."""

from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Encapsulates locators and interactions for the Products/Inventory Page."""

    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_IMAGE = (By.CSS_SELECTOR, ".inventory_item_img img")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    ACTIVE_OPTION = (By.CLASS_NAME, "active_option")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def is_loaded(self) -> bool:
        """Verify the inventory page has loaded and items are visible."""
        return self.is_displayed(self.INVENTORY_LIST)

    def select_sort_option(self, option_text: str) -> None:
        """Sort products using the sort dropdown by visible option text."""
        select_element = self.find_visible(self.SORT_DROPDOWN)
        select = Select(select_element)
        select.select_by_visible_text(option_text)
        # Ensure active option text reflects selection
        self._get_wait().until(
            lambda d: d.find_element(*self.ACTIVE_OPTION).text.strip().lower()
            == option_text.strip().lower()
        )

    def get_product_names(self) -> List[str]:
        """Extract all product titles displayed on the inventory page."""
        elements = self.find_all_visible(self.ITEM_NAME)
        return [el.text.strip() for el in elements]

    def get_product_prices(self) -> List[float]:
        """Extract all product prices as floats, stripping currency symbols."""
        elements = self.find_all_visible(self.ITEM_PRICE)
        return [float(el.text.replace("$", "").strip()) for el in elements]

    def get_product_image_sources(self) -> List[str]:
        """Extract src attribute URLs for all product thumbnails."""
        elements = self.find_all_visible(self.ITEM_IMAGE)
        return [el.get_attribute("src") for el in elements]

    def add_item_to_cart(self, product_name: str) -> None:
        """Add a specific product to the cart by its exact product name."""
        xpath = (
            f"//div[contains(@class, 'inventory_item')]"
            f"[.//div[contains(@class, 'inventory_item_name') and text()='{product_name}']]"
            f"//button"
        )
        button = self.find_visible((By.XPATH, xpath))
        if "add" in button.text.lower():
            button.click()
            # Wait until button switches to Remove state
            self._get_wait().until(
                lambda d: "remove" in d.find_element(By.XPATH, xpath).text.lower()
            )

    def remove_item_from_cart(self, product_name: str) -> None:
        """Remove a specific product from the cart by its exact product name."""
        xpath = (
            f"//div[contains(@class, 'inventory_item')]"
            f"[.//div[contains(@class, 'inventory_item_name') and text()='{product_name}']]"
            f"//button"
        )
        button = self.find_visible((By.XPATH, xpath))
        if "remove" in button.text.lower():
            button.click()
            # Wait until button switches to Add to cart state
            self._get_wait().until(
                lambda d: "add" in d.find_element(By.XPATH, xpath).text.lower()
            )

    def get_cart_badge_count(self) -> int:
        """Return the current cart badge count, or 0 if no badge is rendered."""
        if self.is_displayed(self.CART_BADGE, timeout=2):
            text = self.get_text(self.CART_BADGE)
            return int(text) if text.isdigit() else 0
        return 0

    def open_cart(self) -> None:
        """Click on the shopping cart badge link to open the Cart page."""
        self.click(self.CART_LINK)
