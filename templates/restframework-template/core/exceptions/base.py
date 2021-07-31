from rest_framework import status


class MyException(Exception):
    # default is 400
    http_code = status.HTTP_400_BAD_REQUEST

    @property
    def code(self):
        raise NotImplementedError

    @property
    def msg(self):
        raise NotImplementedError


class NotFound(MyException):
    http_code = status.HTTP_404_NOT_FOUND
    code = 'not_found'
    msg = 'not_found'
