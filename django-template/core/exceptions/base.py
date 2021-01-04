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
