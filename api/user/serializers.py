from rest_framework import serializers

from .models import CustomUser
from marketplace.models import Title, Avatar
from marketplace.serializers import TitleSerializer, AvatarSerializer

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializers for each model/entity in the api - users.
    """
    url = serializers.HyperlinkedIdentityField(view_name="users-detail") # links to the basename used in user.urls.py
    titles = TitleSerializer(many=True)
    avatars = AvatarSerializer(many=True)


    class Meta:
        model = CustomUser
        fields = ['url', 'id','username', 'level', 'experience_points', 'shop_points', 'current_title_id', 'current_avatar_id', 'is_admin', 'titles', 'avatars']
    
    def create(self, validated_data):
        titles_data = validated_data.pop('titles', None)
        avatars_data = validated_data.pop('avatars', None)
        user = CustomUser.objects.create(**validated_data)
                
        if titles_data is not None or avatars_data is not None:
            if titles_data is not None: 
                for title_data in titles_data:
                    Title.objects.get(**title_data)
                    
            if avatars_data is not None:
                for avatar_data in avatars_data:
                    Avatar.objects.get(**avatar_data)
                    
        return user
    
    def update(self, instance, validated_data):
        titles_data = validated_data.pop('titles', None)
        avatars_data = validated_data.pop('avatars', None)
        
        instance = super().update(instance, validated_data)
        
        if titles_data is not None or avatars_data is not None:
            if titles_data is not None:
                instance.titles.clear()    
                for title_data in titles_data:
                    title = Title.objects.get(**title_data)
                    instance.titles.add(title)
                    
            if avatars_data is not None:
                instance.avatars.clear()    
                for avatar_data in avatars_data:
                    avatar = Avatar.objects.get(**avatar_data)
                    instance.avatars.add(avatar)
                    
            return instance