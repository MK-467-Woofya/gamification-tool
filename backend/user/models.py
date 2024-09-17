from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    CustomUser class extending the Django user authentication User class.
    """
    title = models.CharField("User title", max_length=100)
    level = models.IntegerField("Account level", default=1)
    points_accumulated = models.IntegerField("Total points user has accumulated", default=0)
    points_spendable = models.IntegerField("Points remaining for shop currency", default=0)
    
    def __str__(self):
        return self.username


class PointsLog(models.Model):
    """
    用于记录用户积分变化的模型，保存积分和时间。
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points_accumulated = models.IntegerField(default=0)
    points_spendable = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)  # time of changing score

    class Meta:
        ordering = ['-created_at']  # reverse chronological

    def __str__(self):
        return f"{self.user.username} - {self.points_accumulated} - {self.created_at}"
    

@transaction.atomic  # 确保事务的原子性
def update_user_points(user, points_accumulated_delta, points_spendable_delta):
    """
    更新用户的总积分并记录积分变化。
    """
    # 检查可用积分是否为负数
    if user.points_spendable + points_spendable_delta < 0:
        raise ValueError("Insufficient spendable points")

    # 更新用户的总积分
    user.points_accumulated += points_accumulated_delta
    user.points_spendable += points_spendable_delta
    user.save()

    # 记录积分变化
    PointsLog.objects.create(
        user=user,
        points_accumulated=user.points_accumulated,
        points_spendable=user.points_spendable
    )
