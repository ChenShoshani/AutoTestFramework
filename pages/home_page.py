"""
Home page object for Ynet website.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config import get_base_url


class HomePage(BasePage):
    """Home page object for Ynet website."""
    
    LOGO = (By.CSS_SELECTOR, "img[alt*='ynet'], a[href*='ynet'], img[src*='logo']")
    MAIN_CONTENT = (By.TAG_NAME, "main")
    NEWS_ARTICLES = (By.CSS_SELECTOR, "article, .article, [class*='story'], [class*='news']")
    
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
            headline_selectors = ["h1", "h2", ".headline", "[class*='title']"]
            for selector in headline_selectors:
                try:
                    element = self.find_element((By.CSS_SELECTOR, selector))
                    text = element.text.strip()
                    if text:
                        return text
                except:
                    continue
            return ""
        except:
            return ""
    
    def get_article_count(self):
        """Get the number of news articles on the page."""
        try:
            articles = self.driver.find_elements(*self.NEWS_ARTICLES)
            return len(articles)
        except:
            return 0
    
    def verify_page_loaded(self):
        """Verify that the homepage has loaded correctly."""
        try:
            title_ok = "ynet" in self.get_title().lower()
            page_ready = self.driver.execute_script("return document.readyState") == "complete"
            body_exists = len(self.driver.find_elements(By.TAG_NAME, "body")) > 0
            return title_ok and page_ready and body_exists
        except:
            return False 