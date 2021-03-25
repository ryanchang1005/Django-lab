from django.db import models


class ShortURL(models.Model):
    # 短連結的code, ex : https://sh.ort/a09Jwfe/
    code = models.CharField(
        max_length=7,
        unique=True,
    )

    # 完整連結
    url = models.URLField()

    # 建立時間
    create_time = models.DateTimeField(auto_now_add=True)
