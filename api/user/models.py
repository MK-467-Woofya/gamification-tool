from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class CustomUserManager(BaseUserManager):
    """
    Custom UserManager model class
    """
    def create_user(self, username, level=1, title=None, experience_points=0, shop_points=0, password=None):
        """
        Create a user with only their username, and gamification fields 
        """
        if not username:
            raise ValueError("User must have username")
        
        user = self.model(
            username=username,
            level = level,
            experience_points = experience_points,
            shop_points = shop_points,
            title = title,
            #titles = titles,
            #milestones = milestones,
            #badges = badges,
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
    title = models.CharField("User title",max_length=100, blank=True, null=True)
    #titles = models.ForeignKey(titles, on_delete=models.CASCADE)
    #milestones = models.ForeignKey(milestones, on_delete=models.CASCADE)
    #badges = models.ForeignKey(badges, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
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