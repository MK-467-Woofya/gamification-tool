import math
from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from marketplace.models import Title, Avatar


class CustomUserManager(BaseUserManager):
    """
    Custom UserManager model class
    """
    def create_user(self, username, level=1, experience_points=0, shop_points=0, password=None, location=None, is_admin=False, **extra_fields):
        """
        Create a user with only their username, and gamification fields
        """
        if not username:
            raise ValueError("User must have username")

        user = self.model(
            username=username,
            level=level,
            experience_points=experience_points,
            shop_points=shop_points,
            location=location,
            is_admin=is_admin,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Create custom superuser for admin
        """
        user = self.create_user(
            username=username,
            password=password,
            is_admin=True,
            is_superuser=True,  # set is_superuser=True
        )
        user.save(using=self._db)  # fix self.db to self._db
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    CustomUser class
    Built on an overloaded User class.
    A CustomUser object stores information specifically about user gamification aspects.
    The username field is intended to be the username field from the main Woofya application.
    CustomUsers do not require passwords authentication as they are users created as an extension of the Woofya user.
    Most fields are self-explanatory. But some do bear explanation to save confusion:
        - shop_points refer to the spendable currency, experience_points are the cumulative total
        - level is based on the experience_points of a user
    """
    CITY_CHOICES = [
        ('Melbourne', 'Melbourne'),
        ('Sydney', 'Sydney'),
    ]
    username = models.CharField(
        verbose_name="Username",
        max_length=255,
        unique=True,
    )
    level = models.IntegerField("User level", default=1, null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])
    experience_points = models.IntegerField("Experience points", default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999)])
    shop_points = models.IntegerField("Shop points", default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999)])
    location = models.CharField("Location", max_length=100, choices=CITY_CHOICES, blank=True, null=True)  # Optional location field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    current_title = models.ForeignKey(Title, null=True, blank=True, on_delete=models.CASCADE)
    current_avatar = models.ForeignKey(Avatar, null=True, blank=True, on_delete=models.CASCADE)
    titles = models.ManyToManyField(Title, related_name='users', blank=True, default=list)
    avatars = models.ManyToManyField(Avatar, related_name='users', blank=True, default=list)
    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def calculate_level(self) -> int:
        """Formula for calculating user level based on experience_points"""
        return math.floor(0.1 * math.sqrt(self.experience_points)) + 1

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_admin or self.is_superuser

    @property
    def is_staff(self):
        return self.is_admin


class FriendList(models.Model):  # this is a many to many relation linking with user model
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="friend_list")
    friends = models.ManyToManyField(CustomUser, related_name="friends", blank=True)

    def __str__(self):
        return f"{self.user.username}'s friend list"


class PointsLog(models.Model):
    """Class for generating a record of points gained"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    experience_points = models.IntegerField(default=0)
    shop_points = models.IntegerField(default=0)
    # created_at = models.DateTimeField(default=timezone.now)  time of changing score
    created_at = models.DateTimeField(default=timezone.now, editable=True)

    class Meta:
        ordering = ['-created_at']  # reverse chronological

    def __str__(self):
        return f"{self.user.username} - {self.experience_points} - {self.created_at}"


@transaction.atomic
def update_user_points(user, experience_points_delta, shop_points_delta):
    """Transaction handling adding of points, and points log operations"""
    # check if available
    if user.shop_points + shop_points_delta < 0:
        raise ValueError("Insufficient spendable points")

    # points max-value validations
    # case: both points types are at max-value
    if user.experience_points + experience_points_delta >= 9999999 and user.shop_points + shop_points_delta >= 9999999:
        user.experience_points = 9999999
        user.shop_points = 9999999
    # case: user exp points at max-value
    elif user.experience_points + experience_points_delta >= 9999999:
        user.experience_points = 9999999
        user.shop_points += shop_points_delta
    # case: user shop points at max-value
    elif user.shop_points + shop_points_delta >= 9999999:
        user.experience_points += experience_points_delta
        user.shop_points = 9999999
    # case: both points types within max threshold
    else:
        user.experience_points += experience_points_delta
        user.shop_points += shop_points_delta

    # Update users level
    user.level = user.calculate_level()

    # update user points
    user.save()

    # record score change
    PointsLog.objects.create(
        user=user,
        experience_points=user.experience_points,
        shop_points=user.shop_points
    )


@receiver(post_save, sender=CustomUser)
def create_initial_points_log(sender, instance, created, **kwargs):
    """Create a points log after saving CustomUser"""
    if created:
        PointsLog.objects.create(
            user=instance,
            experience_points=instance.experience_points,
            shop_points=instance.shop_points
        )
