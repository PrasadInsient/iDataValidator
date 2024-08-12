import re
def replace_non_ascii(obj):
    """Recursively replace non-ASCII characters in strings within JSON-like objects."""
    if isinstance(obj, dict):
        return {key: replace_non_ascii(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [replace_non_ascii(element) for element in obj]
    elif isinstance(obj, str):
        return re.sub(r'[^\x00-\x7F]', '-', obj)
    else:
        return obj