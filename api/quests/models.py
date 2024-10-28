from django.db import models
from django.contrib.auth import get_user_model

class Quest(models.Model):
    title = models.CharField(max_length=255)
    goal = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    rewards = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class UserQuestProgress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    progress = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
    rewards_claimed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.quest.title} ({self.progress}/{self.quest.goal})"