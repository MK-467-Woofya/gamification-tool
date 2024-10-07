from django.contrib import admin
from .models import Title, Avatar


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'text', 'cost', 'is_listed')
    search_fields = ('id', 'name')
    

class AvatarAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'img_url', 'cost', 'is_listed')
    search_fields = ('id', 'name')


# Register your models here.
admin.site.register(Title, TitleAdmin)
admin.site.register(Avatar, AvatarAdmin)