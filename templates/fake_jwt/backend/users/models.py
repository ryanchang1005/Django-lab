from django.contrib.auth.models import User
from django.db import models

from core.models import AutoPubIDField


class UserDetail(models.Model):
    # 對外ID
    pub_id = AutoPubIDField(
        db_index=True,
    )

    # User物件
    auth_user = models.OneToOneField(
        User,
        on_delete=models.PROTECT
    )
