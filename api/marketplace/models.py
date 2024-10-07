from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField("Name of marketplace item", max_length=50, unique=True)
    cost = models.IntegerField("Price in shop_points", default=0)
    partner = models.CharField("Name of collaborator", max_length=50, blank=True, null=True)
    description = models.CharField("Description of the item", max_length=255, blank=True, null=True)
    date_time_added = models.DateTimeField("When ttem was added to the marketplace", auto_now_add=True)
    is_listed = models.BooleanField("Is item purchaseable?", default=False)
    date_time_listed = models.DateTimeField("Datetime when item was listed", blank=True, null=True)
    date_time_unlisted = models.DateTimeField("Datetime when item became unlisted", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
    

class Title(Item):
    text = models.CharField("Title text", max_length=50, null=True, blank=True)
    

class Avatar(Item):
    img_url = models.ImageField("URL of image", upload_to='avatars', height_field=None, width_field=None, max_length=None, null=True, blank=True)
