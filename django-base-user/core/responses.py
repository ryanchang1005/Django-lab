from django.http.response import JsonResponse

from core.exceptions.middleware import (InvalidToken, InvalidSignature, )


def generate_response_from_middleware_exception(middleware_exception):

    return JsonResponse(
        {
            'http_code': middleware_exception.http_code,
            'error': {
                'code': middleware_exception.code,
                'message': middleware_exception.msg
            }
        },
        status=middleware_exception.http_code,
    )


ResponseInvalidToken = generate_response_from_middleware_exception(InvalidToken)
ResponseInvalidSignature = generate_response_from_middleware_exception(InvalidSignature)