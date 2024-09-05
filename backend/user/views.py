from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CustomUserSerializer, GroupSerializer
from .models import CustomUser

class CustomerUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        users = CustomUser.objects.filter(is_superuser=False).order_by('-points_accumulated')[:10]  # get top 10 user and without superusers
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
