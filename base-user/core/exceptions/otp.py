from rest_framework import status

from .base import MyException


class OtpLost(MyException):
    code = 'otp_lost'
    msg = 'otp expire or not exist'


class OtpInvalid(MyException):
    code = 'otp_invalid'
    msg = 'otp invalid'
