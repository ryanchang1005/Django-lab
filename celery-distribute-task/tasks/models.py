from django.db import models

# Create your models here.
from core.utils import node_generator


class Task(models.Model):
    done_time = models.DateTimeField(
        null=True
    )

    node = models.PositiveSmallIntegerField(default=node_generator)
