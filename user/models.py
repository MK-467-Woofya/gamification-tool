from django.db import models
from django.contrib.auth.models import AbstractUser
"""
CustomUser class extending the Django user authentication User class
"""
class CustomUser(AbstractUser):
    title = models.CharField("User title",max_length=100)
    level = models.IntegerField("Account level", default=1)
    points_accumulated = models.IntegerField("Total points user has accumulated", default=0)
    points_spendable = models.IntegerField("Points remaining for shop currency", default=0)
    
    def __str__(self):
        return self.username