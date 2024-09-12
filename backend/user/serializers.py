from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import CustomUser

# Serializaers for each model/entity

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    url = serializers.HyperlinkedIdentityField(view_name="users-detail") # links to the basename used in user.urls.py
    class Meta:
        model = CustomUser
        fields = ['id','url','username','email', 'groups', 'first_name', 'last_name', 'title', 'level', 'points_accumulated', 'points_spendable']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="groups-detail") # links to the basename used in user.urls.py
    class Meta:
        model = Group
        fields = ['url', 'name']
