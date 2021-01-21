import secrets

def token_generator():
    return secrets.token_hex(64)