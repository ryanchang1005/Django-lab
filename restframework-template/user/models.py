from django.contrib.auth.models import User
from django.db import models


class Permission(models.Model):
    admin_permission_list = [

    ]
    rider_permission_list = [

    ]

    # 權限名稱
    name = models.CharField('name', max_length=80, unique=True)


class Role(models.Model):
    ADMIN = 'admin'
    MY_USER = 'my_user'

    ROLE_CHOICE = (
        (ADMIN, 'admin'),
        (MY_USER, 'my_user'),
    )

    name = models.CharField('name', max_length=50, unique=True)

    users = models.ManyToManyField(
        User,
        verbose_name='users'
    )

    permissions = models.ManyToManyField(
        Permission,
        verbose_name='permissions'
    )


class MyUser(models.Model):
    auth_user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )

    email = models.EmailField(
        unique=True
    )

    display_name = models.CharField(
        max_length=50,
    )

    api_key = models.CharField(
        max_length=40,
        db_index=True,
        unique=True,
        null=True
    )
