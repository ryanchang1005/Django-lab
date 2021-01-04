import json

from django.utils.deprecation import MiddlewareMixin

from core.decorators import un_authenticate_api_exempt
from core.responses import ResponseInvalidUts, ResponseInvalidToken
from core.services.log import LogService
from core.utils.datetime import get_uts
from user.models import Role
from user.services.user import UserService


class UtsCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            if request.method in {'GET', 'DELETE'}:
                # get uts from GET, DELETE params
                uts_str = request.GET.get('uts')
                if uts_str is None:
                    return ResponseInvalidUts
                uts = int(uts_str)
            else:
                # get uts from POST,PUT,PATCH params
                request_body = request.body if request.body else "{}"
                uts = int(json.loads(request_body)['uts'])

            uts_now = get_uts()
            gap_of_milliseconds = uts_now - uts

        except Exception as e:
            return ResponseInvalidUts


class TokenCheckMiddleware(MiddlewareMixin):

    @un_authenticate_api_exempt
    def process_request(self, request):
        try:
            raw_token = request.META.get('HTTP_X_MY_TOKEN')
            user_role, token = raw_token.split()
            user_role = user_role.lower()

            if user_role == Role.ADMIN:
                return ResponseInvalidToken
            elif user_role == Role.MY_USER:

                my_user = UserService.filter(api_key=token).first()

                if my_user is None:
                    return ResponseInvalidToken

                request.user = my_user.auth_user
                request.my_user = my_user
            else:
                return ResponseInvalidToken

        except Exception as e:
            return ResponseInvalidToken


class LogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        LogService.log_middleware(request)
