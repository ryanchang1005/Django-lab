from django.contrib.auth.models import User
from django.db import transaction

from core.exceptions.user import UserAlreadyExist, LoginFailed
from core.utils.string import is_empty
from core.utils.token import generate_token
from user.models import MyUser


class UserService:

    @staticmethod
    def filter(
            qs=None,
            pk=None,
            user=None,
            email=None,
            api_key=None,
    ):
        if qs is None:
            qs = MyUser.objects.all()

        if not is_empty(pk):
            qs = qs.filter(id=pk)

        if user is not None:
            qs = qs.filter(auth_user=user)

        if not is_empty(email):
            qs = qs.filter(email=email)

        if not is_empty(api_key):
            qs = qs.filter(api_key=api_key)

        return qs

    @staticmethod
    def create(
            email,
            password
    ):
        if User.objects.filter(username=email).exists():
            raise UserAlreadyExist

        with transaction.atomic():
            auth_user = User.objects.create_user(
                username=email,
                password=password
            )

            my_user = MyUser()
            my_user.auth_user = auth_user
            my_user.email = email
            my_user.display_name = email
            my_user.api_key = generate_token(40)
            my_user.save()
            return my_user

    @staticmethod
    def login(
            email,
            password
    ):
        my_user = UserService.filter(email=email).first()

        if my_user is None:
            raise LoginFailed

        auth_user = my_user.auth_user

        if not auth_user.check_password(password):
            raise LoginFailed

        my_user.api_key = generate_token(40)
        my_user.save(update_fields=['api_key'])
        return my_user

    @staticmethod
    def logout(my_user):
        my_user.api_key = None
        my_user.save(update_fields=['api_key'])

    @staticmethod
    def edit(
            my_user,
            display_name=None,
    ):
        update_fields = []

        if display_name:
            my_user.display_name = display_name
            update_fields.append('display_name')

        my_user.save(update_fields=update_fields)
        return my_user
