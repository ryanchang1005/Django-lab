from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

from core.decorators import request_exempt
from core.services.fake_jwt import FakeJWTService

InvalidTokenResponse = JsonResponse(data={'code': 'invalid_token'}, status=status.HTTP_403_FORBIDDEN)


class VerifyJWTTokenMiddleware(MiddlewareMixin):

    @request_exempt
    def process_request(self, request):
        raw_token = request.META.get('Authorization')
        _, access_token = raw_token.split()

        if not FakeJWTService.is_access_token_valid(access_token):
            return InvalidTokenResponse

        val = FakeJWTService.decode_access_token_data(access_token)

        user = User.objects.filter(userdetail__pub_id=val['user_id']).first()
        request.user_object = user
