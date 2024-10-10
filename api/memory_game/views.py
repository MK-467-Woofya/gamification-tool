from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.models import CustomUser, update_user_points

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_score(request):
    username = request.data.get('username')
    score = request.data.get('score')

    if not username or score is None:
        return Response({'error': 'Username and score are required'}, status=400)

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)

    # Update user points, assume each match gives 10 experience points
    total_experience = int(score) * 10
    update_user_points(user, total_experience, 0)  # Use positional arguments
    return Response({'message': 'Score submitted successfully'})
