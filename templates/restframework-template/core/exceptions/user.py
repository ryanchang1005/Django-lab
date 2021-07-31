from rest_framework import status

from core.exceptions.base import MyException


class LoginFailed(MyException):
    http_code = status.HTTP_401_UNAUTHORIZED
    code = 'login_failed'
    msg = 'Login fail'


class UserNotLogin(MyException):
    http_code = status.HTTP_401_UNAUTHORIZED
    code = 'user_not_login'
    msg = 'User not login'


class UserAlreadyExist(MyException):
    http_code = status.HTTP_404_NOT_FOUND
    code = 'user_already_exist'
    msg = 'user_already_exist'
