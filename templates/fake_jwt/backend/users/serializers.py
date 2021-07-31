from django.contrib.auth.models import User
from rest_framework import serializers

from core.exceptions.user import LoginFailed
from core.services.fake_jwt import FakeJWTService
from core.utils.datetime import get_now_datetime_obj


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.JSONField()

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        user = User.objects.filter(username=username).first()

        if not user:
            raise LoginFailed

        if not user.check_password(password):
            raise LoginFailed

        user.last_login = get_now_datetime_obj()
        user.save(update_fields=['last_login'])

        return user

    def to_representation(self, instance):
        access_token = FakeJWTService.generate_access_token(instance)
        return {
            'user_id': instance.userdetail.pub_id,
            'access_token': access_token,
        }
