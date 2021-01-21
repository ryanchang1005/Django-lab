from django.db import models


class Config(models.Model):
    distribute_task_count = models.PositiveSmallIntegerField(default=1)
