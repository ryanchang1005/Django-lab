from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import AutoPubIDField


class Chat(models.Model):
    """
    聊天室
    ID, 建立時間
    """

    # 系統編號
    pub_id = AutoPubIDField(
        _('public_id'),
        db_index=True,
    )

    # 建立時間
    create_time = models.DateTimeField(
        _('create_time'),
        auto_now_add=True,
    )


class ChatMessage(models.Model):
    """
    在聊天室的訊息
    哪個聊天室, 什麼名字, 訊息, 什麼時候
    """

    # 聊天室
    chat = models.ForeignKey(
        Chat,
        on_delete=models.PROTECT,
    )

    # 名稱
    name = models.CharField(
        _('name'),
        max_length=32
    )

    # 訊息
    message = models.CharField(
        _('message'),
        max_length=256,
    )

    # 建立時間
    create_time = models.DateTimeField(
        _('create_time'),
    )
