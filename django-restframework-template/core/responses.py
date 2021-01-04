from django.http.response import JsonResponse

from core.exceptions.middleware import InvalidToken, InvalidUts, ExceedRateLimit


def generate_response_from_middleware_exception(middleware_exception):
    return JsonResponse(
        {
            'error': {
                'code': middleware_exception.code,
                'message': middleware_exception.msg
            }
        },
        status=middleware_exception.http_code,
    )


ResponseInvalidToken = generate_response_from_middleware_exception(InvalidToken)
ResponseInvalidUts = generate_response_from_middleware_exception(InvalidUts)
ResponseExceedRateLimit = generate_response_from_middleware_exception(ExceedRateLimit)
