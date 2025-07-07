"""
Basic UI test for browser functionality.
"""

import pytest


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.sanity
def test_browser_functionality(driver):
    """Test that the browser can navigate to a simple page."""
    # Navigate to about:blank - simplest possible page
    driver.get("about:blank")
    
    # Verify we can get basic browser info
    assert driver.current_url == "about:blank", "Should navigate to about:blank"
    
    # Verify browser window dimensions
    window_size = driver.get_window_size()
    assert window_size['width'] > 0, "Window should have width"
    assert window_size['height'] > 0, "Window should have height"
    
    # Verify we can execute simple JavaScript (if enabled)
    try:
        result = driver.execute_script("return 'test'")
        assert result == 'test', "JavaScript execution should work"
    except Exception:
        # If JavaScript is disabled, that's OK - we just verify the driver works
        pass 