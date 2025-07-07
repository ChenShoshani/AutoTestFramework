"""
UI tests for Ynet website search functionality.
"""

import pytest
from pages.home_page import HomePage
from utils.config import load_config
from utils.test_data import get_default_search_term


@pytest.mark.ui
@pytest.mark.sanity
def test_ynet_homepage_loads(driver):
    """Test that Ynet homepage loads successfully."""
    config = load_config()
    driver.get(config["base_url"])
    
    homepage = HomePage(driver)
    
    # Verify page loaded correctly
    assert homepage.verify_page_loaded(), "Ynet homepage should load successfully"
    
    # Verify title contains ynet
    title = homepage.get_title()
    assert "ynet" in title.lower(), "Page title should contain 'ynet'"


@pytest.mark.ui
@pytest.mark.sanity  
def test_search_functionality(driver):
    """Test search functionality on Ynet website."""
    config = load_config()
    driver.get(config["base_url"])
    
    homepage = HomePage(driver)
    
    # Perform search using default search term from data file
    search_term = get_default_search_term()
    homepage.search(search_term)
    
    # Verify search term appears in page source or URL changed
    current_url = driver.current_url
    page_content = driver.page_source
    
    # Check either the search term is in content OR the URL indicates search was performed
    search_performed = (search_term in page_content or 
                       "search" in current_url.lower() or 
                       search_term in current_url)
    
    assert search_performed, "Search should work properly"


@pytest.mark.ui
@pytest.mark.nightly
def test_ynet_basic_navigation(driver):
    """Test basic navigation on Ynet website (nightly test)."""
    config = load_config()
    driver.get(config["base_url"])
    
    homepage = HomePage(driver)
    
    # Verify page elements exist
    assert homepage.verify_page_loaded(), "Homepage should load"
    
    # Check main headline exists
    headline = homepage.get_main_headline()
    assert len(headline) > 0, "Should have main headline"
    
    # Check page title is reasonable
    title = homepage.get_title()
    assert len(title) > 0, "Page should have a title"
    assert "ynet" in title.lower(), "Title should contain 'ynet'" 