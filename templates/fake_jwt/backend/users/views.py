from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.exceptions.user import InvalidUser
from users.serializers import LoginSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    lookup_field = 'pub_id'

    def get_queryset(self):
        if self.action == 'retrieve':
            qs = User.objects.filter(userdetail__pub_id=self.kwargs[self.lookup_field])
        else:
            qs = User.objects.none()
        return qs

    def retrieve(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        user_object = request.user_object

        if user != user_object:
            raise InvalidUser

        return Response(
            data={
                'username': user.username,
                'last_login_at': int(user.last_login.timestamp() * 1000) if user.last_login else 0,
            },
            status=status.HTTP_200_OK
        )

    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
