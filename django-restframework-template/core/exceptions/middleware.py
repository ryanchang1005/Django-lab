from rest_framework import status

from django.utils.translation import ugettext_lazy as _

from .base import MyException


class InvalidToken(MyException):
    http_code = status.HTTP_403_FORBIDDEN
    code = 'invalid_token'
    msg = _('invalid_token')


class InvalidUts(MyException):
    http_code = status.HTTP_403_FORBIDDEN
    code = 'invalid_uts'
    msg = _('invalid_uts')


class ExceedRateLimit(MyException):
    http_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = 'exceed_rate_limit'
    msg = _('exceed_rate_limit')
