"""Base Page class encapsulating Selenium WebDriverWait helpers and interactions.

No time.sleep() calls are permitted. All synchronization relies on explicit waits.
"""

from pathlib import Path
from datetime import datetime
from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.config import EXPLICIT_WAIT_TIMEOUT, SCREENSHOTS_DIR


class BasePage:
    """Base class for all Page Objects in the framework."""

    def __init__(self, driver: WebDriver, timeout: int = EXPLICIT_WAIT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def _get_wait(self, timeout: int | None = None) -> WebDriverWait:
        """Return a WebDriverWait instance for the specified timeout or default."""
        return WebDriverWait(self.driver, timeout if timeout is not None else self.timeout)

    def find_visible(self, locator: Tuple[str, str], timeout: int | None = None) -> WebElement:
        """Wait for element to be visible and return it."""
        wait = self._get_wait(timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def find_all_visible(self, locator: Tuple[str, str], timeout: int | None = None) -> List[WebElement]:
        """Wait for at least one element to be visible and return all visible matching elements."""
        wait = self._get_wait(timeout)
        return wait.until(EC.visibility_of_all_elements_located(locator))

    def find_present(self, locator: Tuple[str, str], timeout: int | None = None) -> WebElement:
        """Wait for element to be present in DOM and return it."""
        wait = self._get_wait(timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_all_present(self, locator: Tuple[str, str], timeout: int | None = None) -> List[WebElement]:
        """Wait for elements to be present in DOM and return list."""
        wait = self._get_wait(timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: Tuple[str, str], timeout: int | None = None) -> None:
        """Wait for element to be clickable and click it."""
        wait = self._get_wait(timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: int | None = None,
        clear_first: bool = True,
    ) -> None:
        """Wait for input field to be visible, optionally clear it, and type text."""
        element = self.find_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str], timeout: int | None = None) -> str:
        """Wait for element to be visible and return its text content."""
        element = self.find_visible(locator, timeout)
        return element.text

    def is_displayed(self, locator: Tuple[str, str], timeout: int = 3) -> bool:
        """Check if an element is visible within the given timeout without throwing TimeoutException."""
        try:
            wait = self._get_wait(timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_attribute(self, locator: Tuple[str, str], attribute_name: str, timeout: int | None = None) -> str | None:
        """Wait for element to be visible and return an attribute value."""
        element = self.find_visible(locator, timeout)
        return element.get_attribute(attribute_name)

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url

    def wait_for_url_contains(self, fragment: str, timeout: int | None = None) -> bool:
        """Wait until current URL contains the expected substring."""
        wait = self._get_wait(timeout)
        return wait.until(EC.url_contains(fragment))

    def take_screenshot(self, name: str) -> Path:
        """Capture a screenshot and save it into the screenshots directory."""
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        file_path = SCREENSHOTS_DIR / filename
        self.driver.save_screenshot(str(file_path))
        return file_path
