#!/usr/bin/env python3


# Code smell: God function
def process_everything(data, config, logger):
    """Function that does too many things"""
    # Validation
    if not data:
        print("No data")  # Should use logger
        return None

    # Processing
    result = []
    for item in data:
        if item > 5:  # Magic number
            result.append(item * 2)  # Magic number

    # Logging
    print(f"Processed {len(result)} items")

    # File I/O
    with open("output.txt", "w") as f:
        f.write(str(result))

    return result


# Modernization opportunity: Could use dataclass
class UserData:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def to_dict(self):
        return {"name": self.name, "email": self.email, "age": self.age}
