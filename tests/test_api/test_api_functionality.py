"""
Basic API test for search functionality.
"""

import pytest
from api.search_client import SearchClient


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.sanity
def test_get_posts():
    """Test that we can get posts from the API."""
    # Create search client
    client = SearchClient()
    
    # Get posts
    response = client.get_posts()
    
    # Verify response
    assert response.status_code == 200, "API should return 200 status"
    
    # Verify response has data
    posts = response.json()
    assert isinstance(posts, list), "Response should be a list"
    assert len(posts) > 0, "Should return some posts"


@pytest.mark.api
@pytest.mark.nightly
def test_get_single_post():
    """Test that we can get a single post by ID."""
    # Create search client
    client = SearchClient()
    
    # Get specific post
    response = client.get_post_by_id(1)
    
    # Verify response
    assert response.status_code == 200, "API should return 200 status"
    
    # Verify post data
    post = response.json()
    assert post["id"] == 1, "Post ID should match requested ID"
    assert "title" in post, "Post should have a title"
    assert "body" in post, "Post should have a body"


@pytest.mark.api
@pytest.mark.nightly
def test_get_users_comprehensive():
    """Comprehensive API test for users endpoint (nightly test)."""
    # Create search client
    client = SearchClient()
    
    # Get users
    response = client.search_users()
    
    # Verify response
    assert response.status_code == 200, "Users API should return 200 status"
    
    # Verify response structure
    users = response.json()
    assert isinstance(users, list), "Users response should be a list"
    assert len(users) > 0, "Should return some users"
    
    # Verify first user structure
    first_user = users[0]
    required_fields = ["id", "name", "email", "username"]
    for field in required_fields:
        assert field in first_user, f"User should have '{field}' field"
    
    # Verify data types
    assert isinstance(first_user["id"], int), "User ID should be integer"
    assert isinstance(first_user["name"], str), "User name should be string"
    assert "@" in first_user["email"], "Email should contain @ symbol" 