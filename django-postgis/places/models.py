from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=30)
    position = models.GeometryField()
