def is_empty(data):
    if data is None:
        return True

    if isinstance(data, str):
        return len(data.strip()) == 0
    elif isinstance(data, list):
        return len(data) == 0

    return False
