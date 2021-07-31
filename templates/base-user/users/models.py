from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from core.models import CreatedAndModifiedMixin, AutoPubIDField

TYPE_MY_USER = 'MyUser'
TYPE_APP_USER = 'AppUser'


class AppUser(CreatedAndModifiedMixin):
    class Meta:
        verbose_name_plural = 'app_users'
        verbose_name = 'app_user'

    pub_id = AutoPubIDField(
        'public id'
    )

    api_token = models.CharField(
        'api token',
        unique=True,
        max_length=255,
        null=True
    )

    sign_pub_key = models.CharField(
        'verify key',
        unique=True,
        max_length=255
    )

    name = models.CharField(
        'name of app user',
        max_length=128
    )


class MyUser(CreatedAndModifiedMixin, AbstractBaseUser):
    class Meta:
        verbose_name_plural = 'my_users'
        verbose_name = 'my_user'

    USERNAME_FIELD = 'pub_id'  # AbstractBaseUser needed
    EMAIL_FIELD = 'email'  # AbstractBaseUser needed

    pub_id = AutoPubIDField(
        'public id'
    )

    email = models.EmailField(
        'email address',
        unique=True,
        max_length=50
    )

    phone = models.CharField(
        'phone',
        max_length=64
    )

    name = models.CharField(
        'name of user',
        max_length=128
    )

    sign_pub_key = models.CharField(
        'verify key',
        unique=True,
        max_length=255
    )

    api_token = models.CharField(
        'api token',
        unique=True,
        max_length=255,
        null=True
    )

    def __str__(self):
        return f'{self.email}'
