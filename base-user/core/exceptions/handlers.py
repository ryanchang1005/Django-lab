from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response

from core.exceptions.base import MyException


def recursive_transform_error_detail(data, upper_data=None, key=None):
    """
    Transform ErrorDetail object to our custom format.
    """
    if isinstance(data, list):
        for i, _ in enumerate(data):
            recursive_transform_error_detail(_, upper_data=data, key=i)
    elif isinstance(data, dict):
        for k, v in data.items():
            recursive_transform_error_detail(v, upper_data=data, key=k)

    elif isinstance(data, exceptions.ErrorDetail):
        result_dict = {
            'code': data.code,
            'message': data
        }
        if isinstance(upper_data, list):
            upper_data[key] = result_dict
        elif isinstance(upper_data, dict):
            upper_data[key] = result_dict


def my_exception_handler(exc, context):
    if isinstance(exc, MyException):
        return Response(
            data={
                'http_code': exc.http_code,
                'error': {
                    'code': exc.code,
                    'message': exc.msg
                }
            },
            status=exc.http_code
        )
    elif isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, (dict, list)):
            recursive_transform_error_detail(exc.detail)
            data = {
                'http_code': exc.status_code,
                'errors': exc.detail
            }
        else:
            data = {
                'http_code': exc.status_code,
                'error': {
                    'code': exc.detail.code,
                    'message': exc.detail
                }
            }

        return Response(
            data,
            status=exc.status_code
        )
    return None
