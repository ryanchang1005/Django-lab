from users.models import MyUser

from rest_framework import serializers

from users.services import UserService


class UserDisplaySerializer(serializers.Serializer):

    def to_representation(self, instance):
        result = {
            'user_id': instance.pub_id,
            'email': instance.email,
            'phone': instance.phone,
            'name': instance.name
        }
        return result


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    sign_pub_key = serializers.CharField(required=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    sign_pub_key = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    otp_id = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError('email format is not valid')
        return value

    def create(self, validated_data):
        user = UserService.create_user(**validated_data)
        return user
