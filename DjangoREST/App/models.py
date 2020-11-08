from django.db import models


class Game(models.Model):
    g_name = models.CharField(max_length=32)
    g_price = models.FloatField(default=0)