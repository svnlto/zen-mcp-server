#!/usr/bin/env python3
# Helper functions that could be modernized


class DataContainer:
    """Simple data container - could use dataclass"""

    def __init__(self, name, value, category):
        self.name = name
        self.value = value
        self.category = category

    def to_dict(self):
        return {"name": self.name, "value": self.value, "category": self.category}
