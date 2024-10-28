from django.contrib import admin
from .models import CheckInLocation

@admin.register(CheckInLocation)
class CheckInLocationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_name', 'latitude', 'longitude', 'checked_in_at']
    search_fields = ['user__username', 'event_name']
