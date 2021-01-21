from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.exceptions.middleware import InvalidToken
from user.serializers.user import UserLoginSerializer, CreateUserSerializer, EditUserSerializer
from user.services.user import UserService


class UserViewSet(viewsets.ViewSet):

    # def list(self, request):
    #     return Response(
    #         data={'action': 'list'},
    #         status=status.HTTP_200_OK
    #     )
    #
    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        my_user = UserService.create(
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return Response(
            data={
                'user_id': my_user.id,
                'user_token': my_user.api_key
            },
            status=status.HTTP_201_CREATED
        )

    #
    # def retrieve(self, request, pk=None):
    #     rider = RiderService.filter(pk=pk).first()
    #
    #     # check header user and url path user same
    #     if request.user != rider.auth_user:
    #         raise InvalidToken
    #
    #     return Response(
    #         data={
    #             'email': request.user.username,
    #             'display_name': rider.display_name
    #         },
    #         status=status.HTTP_200_OK
    #     )
    #
    def update(self, request, pk=None):
        serializer = EditUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        my_user = UserService.edit(
            my_user=request.my_user,
            display_name=validated_data['display_name']
        )

        return Response(
            data={'display_name': my_user.display_name},
            status=status.HTTP_200_OK
        )

    #
    # def partial_update(self, request, pk=None):
    #     return Response(
    #         data={'action': 'partial_update'},
    #         status=status.HTTP_200_OK
    #     )
    #
    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        my_user = UserService.login(
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return Response(
            data={
                'user_id': my_user.id,
                'user_token': my_user.api_key
            },
            status=status.HTTP_200_OK
        )

    @action(methods=['delete'], detail=False, url_path='logout')
    def logout(self, request):
        UserService.logout(my_user=request.my_user)
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
