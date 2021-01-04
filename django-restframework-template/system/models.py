from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models


class Log(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    data = JSONField(
        default=dict
    )

    created = models.DateTimeField(
        auto_now_add=True
    )
