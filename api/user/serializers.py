from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import CustomUser
from marketplace.models import Title, Avatar
from marketplace.serializers import TitleSerializer, AvatarSerializer

class CustomUserSerializer(WritableNestedModelSerializer):
    """
    Serializers for each model/entity in the api - users.
    """
    url = serializers.HyperlinkedIdentityField(view_name="users-detail") # links to the basename used in user.urls.py
    titles = TitleSerializer(many=True)
    avatars = AvatarSerializer(many=True)


    class Meta:
        model = CustomUser
        fields = ['url', 'id','username', 'level', 'experience_points', 'shop_points', 'current_title_id', 'current_avatar_id', 'is_admin', 'titles', 'avatars']
    