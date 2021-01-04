from functools import wraps

from django.urls import exceptions


def un_authenticate_api_exempt(process_request):
    @wraps(process_request)
    def wrapped(middleware_instance, request):
        try:
            # skip login
            if request.method == 'POST' and request.path == '/api/user/login/':
                return None

            # skip create user
            if request.method == 'POST' and request.path == '/api/user/':
                return None

        except (KeyError, exceptions.NoReverseMatch):  # reverse() except when admin urls ware not loaded
            pass
        return process_request(middleware_instance, request)

    return wrapped
