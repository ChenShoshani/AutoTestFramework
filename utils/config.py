"""
Simple configuration loader.
"""

import json
import os


def load_config(config_path="config/config.json"):
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        raise Exception("Configuration file not found: {}".format(config_path))
    
    with open(config_path, 'r') as file:
        return json.load(file)


def get_base_url():
    """Get the base URL for UI tests."""
    config = load_config()
    return config.get("base_url", "https://www.ynet.co.il")


def get_api_base_url():
    """Get the base URL for API tests.""" 
    config = load_config()
    return config.get("api_base_url", "https://jsonplaceholder.typicode.com")


def get_browser():
    """Get the browser type."""
    config = load_config()
    return config.get("browser", "chrome")


def get_timeout():
    """Get the timeout value."""
    config = load_config()
    return config.get("timeout", 10)


def is_headless():
    """Check if browser should run in headless mode."""
    config = load_config()
    return config.get("headless", False) 