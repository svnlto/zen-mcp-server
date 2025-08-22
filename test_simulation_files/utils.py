#!/usr/bin/env python3
# Utility functions with refactoring opportunities


def calculate_total(items):
    """Calculate total with magic numbers"""
    total = 0
    for item in items:
        if item > 10:  # Magic number
            total += item * 1.1  # Magic number for tax
    return total


def format_output(data, format_type):
    """Format output - duplicate logic"""
    if format_type == "json":
        import json

        return json.dumps(data, ensure_ascii=False)
    elif format_type == "csv":
        return ",".join(str(v) for v in data.values())
    else:
        return str(data)
