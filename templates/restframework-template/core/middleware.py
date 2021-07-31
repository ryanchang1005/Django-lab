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


# class VerifyRateLimitMiddleware(MiddlewareMixin):
#     """
#     驗證API key限制速率
#     5 request per second
#     """

#     @un_authenticate_api_exempt
#     def process_request(self, request):
#         api_key = request.GET.get('api_key')

#         if not RateLimitService.touch_and_return_is_pass(api_key):
#             write_log(
#                 LOGGER_MIDDLEWARE_VERIFY_RATE_LIMIT,
#                 'error',
#                 f'api_key={api_key}'
#             )
#             return ExceedRateLimitResponse


class LogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        LogService.log_middleware(request)

# class LogAPIKeyMiddleware(MiddlewareMixin):
#     """
#     記錄此api_key, ip, url_path紀錄
#     """

#     @django_admin_exempt
#     def process_request(self, request):
#         api_key = request.GET.get('api_key')
#         url_path = request.path
#         ip = self.get_client_ip(request)

#         ec_user = EcUserService.filter(api_key=api_key).first()

#         try:
#             APIKeyLogService.create(
#                 ec_user=ec_user,
#                 ip=ip,
#                 url_path=url_path
#             )
#         except:
#             pass

#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip
