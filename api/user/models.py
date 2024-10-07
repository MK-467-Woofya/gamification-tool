from django.db import models, transaction
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from marketplace.models import Title, Avatar


class CustomUserManager(BaseUserManager):
    """
    Custom UserManager model class
    """
    def create_user(self, username, level=1, experience_points=0, shop_points=0, password=None, location=None, is_admin=False):
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
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Create custom superuser for admin
        """
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self.db)
        return user


class CustomUser(AbstractBaseUser):
    """
    CustomUser class
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
    level = models.IntegerField(
        verbose_name="User level from 1-100",
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1),
        ],
    )

    experience_points = models.IntegerField("Experience points", default=0)
    shop_points = models.IntegerField("Shop points", default=0)
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

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class FriendList(models.Model):  # this is a many to many relation linking with user model
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="friend_list")
    friends = models.ManyToManyField(CustomUser, related_name="friends", blank=True)

    def __str__(self):
        return f"{self.user.username}'s friend list"


class PointsLog(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    experience_points = models.IntegerField(default=0)
    shop_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)  # time of changing score

    class Meta:
        ordering = ['-created_at']  # reverse chronological

    def __str__(self):
        return f"{self.user.username} - {self.experience_points} - {self.created_at}"


@transaction.atomic
def update_user_points(user, experience_points_delta, shop_points_delta):

    # check if available
    if user.shop_points + shop_points_delta < 0:
        raise ValueError("Insufficient spendable points")

    # update total score
    user.experience_points += experience_points_delta
    user.shop_points += shop_points_delta
    user.save()

    # record score change
    PointsLog.objects.create(
        user=user,
        experience_points=user.experience_points,
        shop_points=user.shop_points
    )


@receiver(post_save, sender=CustomUser)
def create_initial_points_log(sender, instance, created, **kwargs):
    if created:
        PointsLog.objects.create(
            user=instance,
            experience_points=instance.experience_points,
            shop_points=instance.shop_points
        )
