from functools import wraps

from django.urls import exceptions


def request_exempt(process_request):
    @wraps(process_request)
    def wrapped(middleware_instance, request):
        try:
            print(request.method)
            print(request.path)
            # skip login
            if request.method == 'POST' and request.path == '/api/users/login/':
                return None

        except (KeyError, exceptions.NoReverseMatch):  # reverse() except when admin urls ware not loaded
            pass
        return process_request(middleware_instance, request)

    return wrapped
