from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=255)
    start_at = models.BigIntegerField()
    period = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class EventException(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='exceptions')
    exception_date = models.BigIntegerField()

    def __str__(self):
        return f'{self.event.name} exception'