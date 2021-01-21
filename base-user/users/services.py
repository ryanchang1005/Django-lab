import random

from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone

from core.models import AutoPubIDField
from core.exceptions.otp import OtpLost, OtpInvalid
from core.exceptions.user import UserAlreadyExist
from core.utils.token import token_generator

from .models import MyUser


class UserService:

    @staticmethod
    def create_user(**fields):
        password = fields.pop('password')
        otp_id = fields.pop('otp_id')
        otp = fields.pop('otp')

        # check otp
        cache_otp = cache.get(f'otp:{otp_id}')

        # expire or not exist
        if not cache_otp:
            raise OtpLost

        # invalid
        if cache_otp != otp:
            raise OtpInvalid

        # check exist
        if MyUser.objects.filter(Q(email=fields.get('email')) | Q(sign_pub_key=fields.get('sign_pub_key'))).count() > 0:
            raise UserAlreadyExist

        user = MyUser(**fields)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def login(user):
        user.api_token = token_generator()
        user.last_login = timezone.now()
        user.save(update_fields=['api_token', 'last_login', 'modified'])
        return user.api_token


class OtpService:

    def __init__(self, *args, **kwargs):
        pass

    def _generate_otp_value(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])

    def send(self, email):
        # generate id, value, text
        otp_id = AutoPubIDField().create_pushid()
        otp_value = self._generate_otp_value()
        otp_text = f'your verification code {otp_value}'

        # send
        print(otp_text)

        # set cache(3 min expire)
        k = f'otp:{otp_id}'
        v = otp_value
        cache.set(k, v, 60 * 3)

        return otp_id
