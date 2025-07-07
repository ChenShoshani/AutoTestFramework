"""
Basic UI test for homepage.
"""

import pytest
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.sanity
def test_homepage_loads(driver):
    """Test that the homepage loads successfully."""
    # Create homepage object
    homepage = HomePage(driver)
    
    # Load the page
    homepage.load()
    
    # Verify page loaded
    assert homepage.verify_page_loaded(), "Homepage should load successfully"
    
    # Verify title contains ynet
    title = homepage.get_title()
    assert "ynet" in title.lower(), "Page title should contain 'ynet'" 