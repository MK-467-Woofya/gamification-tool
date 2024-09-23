from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    DRF serializers for user models
    """
    url = serializers.HyperlinkedIdentityField(view_name='user-detail') # links to the basename used in user.urls.py
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'groups']
