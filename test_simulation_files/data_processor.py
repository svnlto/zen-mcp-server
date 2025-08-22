#!/usr/bin/env python3
def process_data(data):
    """Process incoming data"""
    result = []
    for item in data:
        if item.get("valid"):
            result.append(item["value"])
    return result
