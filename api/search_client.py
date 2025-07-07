"""
Simple API client for search functionality.
"""

import requests
from utils.config import get_api_base_url, get_timeout


class SearchClient:
    """Simple search API client."""
    
    def __init__(self):
        """Initialize the search client."""
        self.base_url = get_api_base_url()
        self.timeout = get_timeout()
    
    def get_posts(self):
        """Get all posts from the API."""
        url = "{}/posts".format(self.base_url)
        response = requests.get(url, timeout=self.timeout)
        return response
    
    def get_post_by_id(self, post_id):
        """Get a single post by ID."""
        url = "{}/posts/{}".format(self.base_url, post_id)
        response = requests.get(url, timeout=self.timeout)
        return response
    
    def search_users(self):
        """Get users from the API."""
        url = "{}/users".format(self.base_url)
        response = requests.get(url, timeout=self.timeout)
        return response 