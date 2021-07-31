from django.shortcuts import render

from rest_framework.viewsets import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers.users import SignUpSerializer, UserDisplaySerializer, LoginSerializer, EmailSerializer

from .models import MyUser

from .services import UserService, OtpService

from core.exceptions.user import LoginFailed


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin, GenericViewSet):
    lookup_filed = 'pub_id'

    def get_queryset(self):
        return MyUser.objects.filter(id=self.request.user_object.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return SignUpSerializer
        elif self.action == 'retrieve':
            return UserDisplaySerializer
        return None

    def retrieve(self, request, *args, **kwargs):
        serializer = UserDisplaySerializer(request.user_object)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = serializer.instance

        return Response(
            data={
                'user_id': user.pub_id
            },
            status=status.HTTP_201_CREATED
        )

    @action(methods=['post'], detail=False)
    def email(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        email = validated_data['email']
        otp_id = OtpService().send(email)

        return Response(
            data={
                'otp_id': otp_id
            },
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            user = MyUser.objects.get(email=validated_data['email'])
        except MyUser.DoesNotExist:
            raise LoginFailed()

        if user.check_password(validated_data['password']):
            user.sign_pub_key = validated_data['sign_pub_key']
            user.save(update_fields=['sign_pub_key', 'modified'])

            api_token = UserService.login(user)
            return Response(
                data={
                    'user_id': user.pub_id,
                    'user_token': api_token
                },
                status=status.HTTP_200_OK
            )
        else:
            raise LoginFailed()
