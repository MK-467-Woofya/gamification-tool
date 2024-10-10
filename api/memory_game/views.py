from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from user.models import CustomUser, update_user_points
from .models import UserMemoryGameScore

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

    # Check if 3 days have passed since last completion
    last_score = UserMemoryGameScore.objects.filter(user=user).order_by('-completed_at').first()

    if last_score:
        time_since_last_play = timezone.now() - last_score.completed_at
        if time_since_last_play < timezone.timedelta(days=3):
            # Do not award points or update last completion time
            message = "Game completed. You did not earn points this time."
            # Still record that the user played the game
            UserMemoryGameScore.objects.create(user=user, score=score)
            return Response({'message': message})
        else:
            # Award points and update last completion time
            update_user_points(user, int(score), 0)
            # Record the game completion
            UserMemoryGameScore.objects.create(user=user, score=score)
            return Response({'message': 'Game completed. Your score has been recorded.'})
    else:
        # First time playing the game, award points
        update_user_points(user, int(score), 0)
        # Record the game completion
        UserMemoryGameScore.objects.create(user=user, score=score)
        return Response({'message': 'Game completed. Your score has been recorded.'})



@api_view(['GET'])
@permission_classes([AllowAny])
def check_game_eligibility(request):
    # Get username from request headers
    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Username '):
        return Response({'error': 'Unauthorized: Username is required'}, status=401)

    username = authorization_header.split(' ')[1]
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)

    # Check the last time the user completed the game
    last_score = UserMemoryGameScore.objects.filter(user=user).order_by('-completed_at').first()

    if last_score:
        time_since_last_completion = timezone.now() - last_score.completed_at
        if time_since_last_completion < timezone.timedelta(days=3):
            # Calculate remaining time
            remaining_time = timezone.timedelta(days=3) - time_since_last_completion
            remaining_seconds = int(remaining_time.total_seconds())
            hours, remainder = divmod(remaining_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            return Response({
                'eligible': True,
                'can_earn_points': False,
                'message': 'You need to wait before earning points again.',
                'remaining_time': {
                    'hours': hours,
                    'minutes': minutes,
                    'seconds': seconds
                }
            })
        else:
            return Response({'eligible': True, 'can_earn_points': True})
    else:
        # User hasn't played the game before
        return Response({'eligible': True, 'can_earn_points': True})
