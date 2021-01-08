from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import JSONField


class PublishingError(models.Model):
    topic = models.CharField(max_length=100)
    payload = JSONField(encoder=DjangoJSONEncoder)
    attributes = JSONField(null=True, encoder=DjangoJSONEncoder)
    bulk = models.BooleanField(default=False)
    error = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
