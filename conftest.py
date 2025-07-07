"""
Pytest configuration and fixtures.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import get_timeout, is_headless


@pytest.fixture(scope="function")
def driver():
    """WebDriver fixture that provides a clean browser instance for each test."""
    # Setup Chrome options
    options = ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    if is_headless():
        options.add_argument("--headless")
    
    # Create driver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(get_timeout())
    
    yield driver
    
    # Cleanup
    driver.quit() 