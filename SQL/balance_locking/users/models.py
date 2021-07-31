import secrets

from django.contrib.auth.models import User
from django.db import models


def generate_salt():
    return secrets.token_urlsafe(20)


class UserDetail(models.Model):
    # User
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    # 餘額, 999999999.00
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # 鹽
    balance_hash_salt = models.CharField(
        max_length=30,
        default=generate_salt
    )

    # Hash
    balance_hash = models.CharField(
        max_length=64,
    )

    # 餘額更新時間
    balance_update_at = models.DateTimeField()


class UserBalanceLog(models.Model):
    # User
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    from_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    to_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created = models.DateTimeField()
