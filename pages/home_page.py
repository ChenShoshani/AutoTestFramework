"""
Home page object for Ynet website.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import get_base_url
from utils.test_data import get_default_search_term


class HomePage(BasePage):
    """Home page object for Ynet website."""
    
    # Page selectors
    LOGO = (By.XPATH, "//img[@aria-label='דף הבית של ynet']")
    MAIN_HEADLINE = (By.CSS_SELECTOR, "h1[class='slotTitle'] span[contenteditable='false']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".searchBtn")
    
    def __init__(self, driver):
        """Initialize the HomePage."""
        super(HomePage, self).__init__(driver)
        self.base_url = get_base_url()
    
    def load(self):
        """Navigate to the homepage."""
        self.open(self.base_url)
    
    def is_logo_displayed(self):
        """Check if the header logo is displayed."""
        return self.is_element_visible(self.LOGO)
    
    def get_main_headline(self):
        """Get the main headline text."""
        try:
            headline = self.find_element(self.MAIN_HEADLINE)
            return headline.text.strip()
        except:
            return ""
    

    
    def verify_page_loaded(self):
        """Verify that the homepage has loaded correctly."""
        try:
            title_ok = "ynet" in self.get_title().lower()
            page_ready = self.driver.execute_script("return document.readyState") == "complete"
            body_exists = len(self.driver.find_elements(By.TAG_NAME, "body")) > 0
            return title_ok and page_ready and body_exists
        except:
            return False
    
    def search(self, search_term=None):
        """Perform search on Ynet website."""
        if search_term is None:
            search_term = get_default_search_term()
        
        # Find and click search button to open search field
        search_button = self.find_element(self.SEARCH_BUTTON)
        search_button.click()
        
        # Wait for search field to open
        import time
        time.sleep(1)
        
        # After clicking, the same element becomes input field - type search term
        search_button.send_keys(search_term)
        
        # Press Enter to execute search
        from selenium.webdriver.common.keys import Keys
        search_button.send_keys(Keys.RETURN)
        
        # Wait a bit for search results
        time.sleep(2) 