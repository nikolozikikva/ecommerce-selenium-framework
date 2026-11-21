"""Pytest configuration, fixtures, and reporting hooks."""

import re
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.config import SCREENSHOTS_DIR


@pytest.fixture(scope="function")
def driver():
    """Initialize a headless Chrome WebDriver instance with clean teardown."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver_instance = webdriver.Chrome(options=options)
    driver_instance.set_page_load_timeout(30)

    yield driver_instance

    driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to capture a timestamped PNG screenshot into screenshots/ on failure."""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        driver_instance = item.funcargs.get("driver")
        if driver_instance:
            SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            clean_name = re.sub(r"[^\w\-_]", "_", item.name)
            filename = f"FAIL_{clean_name}_{timestamp}.png"
            filepath = SCREENSHOTS_DIR / filename
            driver_instance.save_screenshot(str(filepath))

            try:
                from pytest_html import extras as html_extras
                # Embed base64 image in self-contained HTML report
                extras.append(html_extras.png(driver_instance.get_screenshot_as_base64()))
            except Exception:
                pass

    report.extras = extras
