import base64


def base64_encode(s):
    return base64.b64encode(s.encode('UTF-8')).decode('UTF-8')


def base64_decode(s):
    return base64.b64decode(s.encode('UTF-8')).decode('UTF-8')
