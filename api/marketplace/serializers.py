from rest_framework import serializers

from .models import Title, Avatar

class TitleSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializers for Titles.
    """
    url = serializers.HyperlinkedIdentityField(view_name="titles-detail") # links to the basename used in user.urls.py
    class Meta:
        model = Title
        fields = ['url', 'id','name', 'text', 'partner', 'cost', 'description', 'is_listed', 'date_time_added', 'date_time_unlisted']

class AvatarSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializers for Titles.
    """
    url = serializers.HyperlinkedIdentityField(view_name="avatars-detail") # links to the basename used in user.urls.py
    class Meta:
        model = Avatar
        fields = ['url', 'id','name', 'img_url', 'partner', 'cost', 'description', 'is_listed', 'date_time_added', 'date_time_unlisted']
