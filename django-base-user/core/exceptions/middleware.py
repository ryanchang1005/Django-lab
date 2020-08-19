from rest_framework import status

from .base import MyException

class InvalidToken(MyException):

    http_code = status.HTTP_403_FORBIDDEN
    code = 'invalid_token'
    msg = 'invalid_token'


class InvalidSignature(MyException):

    http_code = status.HTTP_403_FORBIDDEN
    code = 'invalid_signature'
    msg = 'invalid_signature'