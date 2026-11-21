"""Page Object for SauceDemo Login Page."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    """Encapsulates locators and interactions for the Login Page."""

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self) -> "LoginPage":
        """Navigate to the SauceDemo base login URL."""
        self.driver.get(BASE_URL)
        self.find_visible(self.USERNAME_INPUT)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        """Type username into the username field."""
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Type password into the password field."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        """Click the login submit button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Execute the full login sequence."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Extract and return text from the error banner."""
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self, timeout: int = 3) -> bool:
        """Check if the error banner is displayed."""
        return self.is_displayed(self.ERROR_CONTAINER, timeout=timeout)
