"""
Basic UI tests for Ynet website functionality.
"""

import pytest
from pages.home_page import HomePage
from utils.config import load_config
from utils.test_data import get_hebrew_indicators


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.sanity
def test_ynet_site_accessibility(driver):
    """Test that Ynet website is accessible and loads properly."""
    config = load_config()
    driver.get(config["base_url"])
    
    # Basic connectivity test
    assert driver.current_url.startswith("https://"), "Should be using HTTPS"
    assert "ynet" in driver.current_url.lower(), "Should be on Ynet domain"
    
    # Check page loads
    page_source = driver.page_source
    assert len(page_source) > 1000, "Page should have substantial content"
    assert "ynet" in page_source.lower(), "Page should contain 'ynet'"
    
    # Check page title
    title = driver.title
    assert len(title) > 0, "Page should have a title"
    

@pytest.mark.ui
@pytest.mark.nightly
def test_ynet_page_elements(driver):
    """Test that basic page elements exist on Ynet homepage.""" 
    config = load_config()
    driver.get(config["base_url"])
    
    homepage = HomePage(driver)
    
    # Test page object functionality
    assert homepage.verify_page_loaded(), "Page should be verified as loaded"
    
    # Test logo visibility
    logo_visible = homepage.is_logo_displayed()
    print(f"Logo visible: {logo_visible}")
    assert logo_visible, "Logo should be visible"
    
    # Test main headline
    headline = homepage.get_main_headline()
    print(f"Main headline: {headline}")
    assert len(headline) > 0, "Should have main headline"
    
    # Basic page structure tests - using data file for Hebrew content
    page_source = driver.page_source.lower()
    
    # Look for Hebrew content using data from JSON file
    hebrew_indicators = get_hebrew_indicators()
    found_indicators = [word for word in hebrew_indicators if word in page_source]
    
    print(f"Found Hebrew indicators: {found_indicators}")
    # Should find Hebrew content on Hebrew news site
    assert len(found_indicators) > 0, f"Should find Hebrew content on Ynet. Found: {found_indicators}"