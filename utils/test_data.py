"""
Simple test data helper - demonstrates data-driven testing without over-engineering.
"""

import json
import os


def load_test_data():
    """Load test data from JSON file."""
    # Get the directory of this script (utils/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root, then into data/
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, "data", "test_data.json")
    
    with open(data_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_default_search_term():
    """Get default search term for testing."""
    data = load_test_data()
    return data["search_terms"]["default"]


def get_hebrew_indicators():
    """Get Hebrew content indicators for validation."""
    data = load_test_data()
    return data["hebrew_content"] 