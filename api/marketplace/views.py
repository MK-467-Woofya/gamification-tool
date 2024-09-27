from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from .serializers import TitleSerializer, AvatarSerializer
from .models import Title, Avatar


class TitleViewSet(viewsets.ModelViewSet):
    """
    API endpoints set that allows Titles to be viewed or edited.
    """
    queryset = Title.objects.all().order_by('-date_time_added')
    serializer_class = TitleSerializer
    
    @action(methods=['GET'], detail=False, url_path='name/(?P<name>\w+)')
    def get_by_title(self, request, name):
        title = get_object_or_404(Title, name=name)
        data = TitleSerializer(title, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, url_path='snippet/')
    def titles_snippet(self, request):
        titles = Title.objects.order_by('-date_time_added')[:10]
        data = TitleSerializer(titles, many=True, context={'request': request})
        return Response(data, status=status.HTTP_200_OK)
    
class AvatarViewSet(viewsets.ModelViewSet):
    """
    API endpoints set that allows Avatars to be viewed or edited.
    """
    queryset = Avatar.objects.all().order_by('-date_time_added')
    serializer_class = AvatarSerializer
    
    
