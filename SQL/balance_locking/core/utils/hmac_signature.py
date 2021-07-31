import hmac

from core.utils.encode_decode import base64_encode


def sign(secret_key, payload):
    return hmac.new(secret_key.encode(), base64_encode(payload).encode(), 'sha256').hexdigest()


def verify(secret_key, payload, signature):
    return sign(secret_key, payload) == signature
