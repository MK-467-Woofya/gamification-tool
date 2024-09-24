from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from .serializers import CustomUserSerializer
from .models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-username')
    serializer_class = CustomUserSerializer
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        users = CustomUser.objects.filter(is_admin=False).order_by('-points_accumulated')[:10]  # get top 10 user and without superusers
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['PATCH'], name="Update points")
    def update_points(self, request, *args, **kwargs):
        """Single user points update"""
        user = self.get_object()
        
        new_experience_points = user.experience_points + int(request.data.get("experience_points"))
        new_shop_points = user.shop_points + int(request.data.get("shop_points"))
        
        data = {"experience_points" : new_experience_points, "shop_points": new_shop_points}
        
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    @action(detail=True, methods=['PATCH'], name="Spend points")
    def spend_points(self, request, *args, **kwargs):
        """Single user points spend"""
        user = self.get_object()
        
        new_shop_points = user.shop_points - int(request.data.get("shop_points"))
        
        data = {"shop_points": new_shop_points}
        
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    @action(methods=['GET'], detail=False, url_path='username/(?P<username>\w+)')
    def getByUsername(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        data = CustomUserSerializer(user, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)
    