from django.contrib.postgres.fields import JSONField
from django.db import models


class PublishingError(models.Model):
    topic = models.CharField(max_length=100)
    payload = JSONField()
    attributes = JSONField(null=True)
    error = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
