from django.db import models
from django.contrib.auth.models import User

class Quest(models.Model):
    title = models.CharField(max_length=255)
    goal = models.IntegerField()  # e.g., total km or number of sessions
    progress = models.FloatField(default=0)  # Track the user's current progress
    user = models.ForeignKey(User, related_name='quests', on_delete=models.CASCADE)  # Link the quest to a user

    def __str__(self):
        return f"{self.title} ({self.progress}/{self.goal})"