"""Tests for product catalog sorting, cart badge counter updates, and known defects."""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config import (
    STANDARD_USER,
    PROBLEM_USER,
    PASSWORD,
)


class TestCartAndSorting:
    """Test suite for product sorting, cart operations, and catalog defects."""

    def test_price_sorting_low_to_high(self, driver):
        """Verify sorting by 'Price (low to high)' orders numeric prices ascending."""
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(STANDARD_USER, PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded(), "Inventory page must be loaded before sorting"

        inventory_page.select_sort_option("Price (low to high)")
        prices = inventory_page.get_product_prices()

        assert len(prices) > 1, f"Expected multiple products, found {len(prices)}"
        assert prices == sorted(prices), (
            f"Prices are not in ascending order: {prices}"
        )

    def test_cart_badge_counter_updates(self, driver):
        """Verify cart badge updates accurately when adding 3 items and removing 1 item."""
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(STANDARD_USER, PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()
        assert inventory_page.get_cart_badge_count() == 0, "Cart badge should initially be empty"

        items_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
        ]

        for item in items_to_add:
            inventory_page.add_item_to_cart(item)

        assert inventory_page.get_cart_badge_count() == 3, (
            f"Expected badge count 3 after adding 3 items, got {inventory_page.get_cart_badge_count()}"
        )

        inventory_page.remove_item_from_cart("Sauce Labs Backpack")
        assert inventory_page.get_cart_badge_count() == 2, (
            f"Expected badge count 2 after removing 1 item, got {inventory_page.get_cart_badge_count()}"
        )

    @pytest.mark.xfail(
        reason="Known UI defect on problem_user: duplicate broken product thumbnails",
        strict=True,
    )
    def test_problem_user_product_images_not_all_broken(self, driver):
        """Defect detection: problem_user renders sl-404 broken images for all products."""
        login_page = LoginPage(driver)
        login_page.load()
        login_page.login(PROBLEM_USER, PASSWORD)

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()

        image_sources = inventory_page.get_product_image_sources()
        assert len(image_sources) > 0, "Expected product images to be present"

        # On problem_user, all image URLs contain 'sl-404', which violates valid product display
        is_all_broken = all("sl-404" in src for src in image_sources)
        assert not is_all_broken, (
            f"Defect reproduced: All {len(image_sources)} product images point to broken sl-404 thumbnail"
        )
