from django.contrib import admin
from .models import CustomUser, FriendList, PointsLog

class FriendListInline(admin.TabularInline):
    model = FriendList.friends.through
    verbose_name = "friend"
    verbose_name_plural = "friends"

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [FriendListInline]
    list_display = ('username', 'email', 'location', 'points_accumulated', 'points_spendable')
    search_fields = ('username', 'location')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FriendList)
admin.site.register(PointsLog)