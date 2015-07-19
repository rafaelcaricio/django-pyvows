from django.db import models


class StringModel(models.Model):
    name = models.CharField(max_length=100)
