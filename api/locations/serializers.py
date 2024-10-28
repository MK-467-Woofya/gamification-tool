from rest_framework import serializers
from .models import CheckInLocation

class CheckInLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInLocation
        fields = ['id', 'user', 'event_name', 'latitude', 'longitude', 'checked_in_at']