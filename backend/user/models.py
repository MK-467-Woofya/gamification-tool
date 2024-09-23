from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUser(AbstractUser):
    """
    CustomUser class extending the Django user authentication User class.
    """

    CITY_CHOICES = [
        ('Melbourne', 'Melbourne'),
        ('Sydney', 'Sydney'),
        # add more locations here
    ]
    title = models.CharField("User title", max_length=100)
    level = models.IntegerField("Account level", default=1)
    points_accumulated = models.IntegerField("Total points user has accumulated", default=0)
    points_spendable = models.IntegerField("Points remaining for shop currency", default=0)
    location = models.CharField("Location", max_length=100, choices=CITY_CHOICES, blank=True, null=True)  # Optional location field

    def __str__(self):
        return self.username
    

class FriendList(models.Model): # this is a many to many relation linking with user model
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="friend_list")
    friends = models.ManyToManyField(CustomUser, related_name="friends", blank=True)

    def __str__(self):
        return f"{self.user.username}'s friend list"



class PointsLog(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points_accumulated = models.IntegerField(default=0)
    points_spendable = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)  # time of changing score

    class Meta:
        ordering = ['-created_at']  # reverse chronological

    def __str__(self):
        return f"{self.user.username} - {self.points_accumulated} - {self.created_at}"
    

@transaction.atomic
def update_user_points(user, points_accumulated_delta, points_spendable_delta):

    # check if available
    if user.points_spendable + points_spendable_delta < 0:
        raise ValueError("Insufficient spendable points")

    # update total score
    user.points_accumulated += points_accumulated_delta
    user.points_spendable += points_spendable_delta
    user.save()

    # record score change
    PointsLog.objects.create(
        user=user,
        points_accumulated=user.points_accumulated,
        points_spendable=user.points_spendable
    )

@receiver(post_save, sender=CustomUser)
def create_initial_points_log(sender, instance, created, **kwargs):
    if created:
        PointsLog.objects.create(
            user=instance,
            points_accumulated=instance.points_accumulated,
            points_spendable=instance.points_spendable
        )