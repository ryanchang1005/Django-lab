from rest_framework import status

from .base import MyException


class LoginFailed(MyException):
    http_code = status.HTTP_401_UNAUTHORIZED
    code = 'login_failed'
    msg = 'login failed'


class UserAlreadyExist(MyException):
    http_code = status.HTTP_409_CONFLICT
    code = 'user_already_exists'
    msg = 'user already exists'
