import logging

from django.utils.deprecation import MiddlewareMixin

from core.cache import get_user_cache_object
from core.responses import (ResponseInvalidToken, )
from core.utils.key import server_sign_pri_key, sign
from users.models import TYPE_MY_USER, TYPE_APP_USER, MyUser

logger = logging.getLogger(__name__)


class TokenCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        raw_token = request.headers.get('X-MY-TOKEN')

        if not raw_token:
            return ResponseInvalidToken

        try:
            user_type, token = raw_token.split()
        except ValueError:
            return ResponseInvalidToken
        else:
            if user_type not in [TYPE_MY_USER, TYPE_APP_USER]:
                return ResponseInvalidToken

        user_cache_object = get_user_cache_object(user_type, token)

        if not user_cache_object:
            return ResponseInvalidToken

        user_object = None

        if user_type == TYPE_MY_USER:
            user_object = MyUser.objects.get(id=user_cache_object.id)

        logger.info(f'user={user_object.id}, in system(TokenCheckMiddleware)')
        request.user_type = user_type
        request.token = token
        request.user_object = user_object
        request.user_cache_object = user_cache_object


class SignMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        logger.info(f'user={request.user_object.id}, out system(SignMiddleware)')
        if response.content:
            response['X-MY-SIGNATURE'] = sign(server_sign_pri_key, response.content.decode())

        return response
