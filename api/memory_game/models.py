from django.db import models
from user.models import CustomUser

class UserMemoryGameScore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    eligible_for_leaderboard = models.BooleanField(default=True)  # New field

    def __str__(self):
        return f"{self.user.username} - {self.score} - {self.completed_at}"
