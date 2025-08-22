#!/usr/bin/env python3
def validate_input(data):
    """Validate input data"""
    if not isinstance(data, list):
        raise ValueError("Data must be a list")

    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Items must be dictionaries")
        if "value" not in item:
            raise ValueError("Items must have 'value' key")

    return True
