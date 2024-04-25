"""
Common utils
"""

import re


PATTERN = r"(?P<item_name>\w+(?: \w+)*) (?P<quantity>\d+(?:\.\d+)?(?:\s?(?:kg|lb|oz|g|ml|L|...))?) (?P<price>\d+(?:\.\d+)?)"
regex = re.compile(PATTERN, flags=re.IGNORECASE)


def parse_item_info(user_input):
    """
    Parses user input in the format "item_name quantity price" and returns a dictionary.
    Args:
        user_input: A string containing item information separated by spaces.
    Returns:
        A dictionary with keys "item_name", "quantity", and "price" or None if parsing fails.
    """
    matches = re.match(regex, user_input)

    if matches:
        return {
            "item_name": matches.group("item_name"),
            "quantity": matches.group("quantity"),
            "price": matches.group("price"),
        }

    return None
