from rest_framework import status

from core.exceptions.base import MyException


class PostNotExist(MyException):
    http_code = status.HTTP_404_NOT_FOUND
    code = 'post_not_exist'
    msg = 'Post not exist'


class PostAuthorInvalid(MyException):
    http_code = status.HTTP_400_BAD_REQUEST
    code = 'post_author_invalid'
    msg = 'Post author invalid'
