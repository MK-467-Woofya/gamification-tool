from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action



from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]
    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
    """API endpoint to retrieve user by username"""
    @action(methods=['get'], detail=False,
            url_path='username/(?P<username>\w+)')
    def getByUsername(self, request, username):
        user = get_object_or_404(User, username=username)
        data = UserSerializer(user, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    """
    API endpoint for logging out user and blacklisting access tokens
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
