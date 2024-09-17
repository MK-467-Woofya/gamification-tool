from django.http import HttpResponse
from user.serializers import CustomUserSerializer
from user.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

def index(request):
    return HttpResponse("Leaderboard index page.")

@api_view(['GET'])
def leaderboard(request):
    users = CustomUser.objects.filter(is_superuser=False).order_by('-points_accumulated')[:10]
    serializer = CustomUserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)

