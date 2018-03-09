from django.db import models
from django.contrib.auth import get_user_model


class StoreLog(models.Model):
    store_user = models.ForeignKey(
        get_user_model(),
        related_name='logs')
    username = models.CharField(max_length=256)
    geek_rank = models.CharField(max_length=256)
    kind = models.CharField(max_length=256)
    created_at = models.CharField(max_length=256)
