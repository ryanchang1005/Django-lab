import secrets


def generate_token(length):
    return secrets.token_hex(int(length / 2))
