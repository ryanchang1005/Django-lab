from django.db import models

from user.models import MyUser


class Post(models.Model):
    title = models.CharField(max_length=100)

    content = models.TextField()

    author = models.ForeignKey(
        MyUser,
        on_delete=models.PROTECT
    )

    created = models.DateTimeField(auto_now_add=True)
