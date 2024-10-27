from django.db import models
from user.models import CustomUser

class CheckInLocation(models.Model):
    user = models.ForeignKey(CustomUser, related_name='checkins', on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    checked_in_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} checked in at {self.event_name}"