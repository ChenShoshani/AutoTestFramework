"""
Simple UI test for search button functionality.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.mark.ui
@pytest.mark.sanity
def test_search_button_exists(driver):
    """Test that search button with class 'searchBtn' exists on page."""
    # Navigate to a test page with search button
    test_html = """
    <html>
        <head><title>Search Test Page</title></head>
        <body>
            <h1>Test Page</h1>
            <input type="text" placeholder="Search..." />
            <button class="searchBtn" id="search-btn">Search</button>
        </body>
    </html>
    """
    
    driver.get(f"data:text/html,{test_html}")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(EC.title_contains("Search Test Page"))
    
    # Verify search button exists with correct class
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "searchBtn"))
        )
        assert search_button is not None, "Search button with class 'searchBtn' should exist"
        assert search_button.is_displayed(), "Search button should be visible"
        assert search_button.text == "Search", "Button should contain 'Search' text"
        
    except TimeoutException:
        pytest.fail("Search button with class 'searchBtn' was not found on the page")


@pytest.mark.ui  
@pytest.mark.nightly
def test_search_button_clickable(driver):
    """Test that search button is clickable (nightly test)."""
    # Navigate to a test page with interactive search button
    test_html = """
    <html>
        <head><title>Interactive Search</title></head>
        <body>
            <h1>Interactive Test</h1>
            <input type="text" id="search-input" placeholder="Enter search term..." />
            <button class="searchBtn" id="search-btn" onclick="this.style.background='green'">Search</button>
        </body>
    </html>
    """
    
    driver.get(f"data:text/html,{test_html}")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(EC.title_contains("Interactive Search"))
    
    # Find and click the search button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "searchBtn"))
    )
    
    # Verify button is clickable
    assert search_button.is_enabled(), "Search button should be enabled"
    
    # Click the button
    search_button.click()
    
    # Verify click worked (button background should change to green)
    button_style = search_button.get_attribute("style")
    assert "green" in button_style.lower(), "Button background should change after click" 