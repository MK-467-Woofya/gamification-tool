from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializers for each model/entity in the api - users.
    """
    url = serializers.HyperlinkedIdentityField(view_name="users-detail")  # links to the basename used in user.urls.py

    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'level', 'experience_points', 'shop_points', 'title', 'is_admin']
