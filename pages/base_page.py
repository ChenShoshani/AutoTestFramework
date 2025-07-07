"""
Base page class for all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config import get_timeout


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver):
        """Initialize the base page."""
        self.driver = driver
        self.wait = WebDriverWait(driver, get_timeout())
    
    def open(self, url):
        """Navigate to a specific URL."""
        self.driver.get(url)
    
    def get_title(self):
        """Get the current page title."""
        return self.driver.title
    
    def find_element(self, locator):
        """Find a single element with explicit wait."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            raise TimeoutException("Element not found: {}".format(locator))
    
    def click_element(self, locator):
        """Click an element with explicit wait."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        """Enter text into an input field."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from an element."""
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator):
        """Check if element is visible."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False 