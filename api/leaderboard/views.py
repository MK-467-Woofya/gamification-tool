from django.http import HttpResponse
from django.utils import timezone

from datetime import timedelta

from rest_framework.response import Response
from rest_framework.decorators import api_view

from user.serializers import CustomUserSerializer
from user.models import CustomUser
from user.models import PointsLog


# get leaderboard by time
def get_leaderboard_by_time_period(start_time):
    logs = PointsLog.objects.filter(created_at__gte=start_time).select_related('user').order_by('-experience_points')
    
    user_scores = {}
    for log in logs:
        if log.user.id not in user_scores:  # user id is key
            user_scores[log.user.id] = {
                'username': log.user.username,
                'experience_points': log.experience_points,
                'shop_points': log.shop_points,
            }
    return sorted(user_scores.values(), key=lambda x: x['experience_points'], reverse=True)


def get_leaderboard_by_time_frame(time_delta):
    start_time = timezone.now() - time_delta
    leaderboard = get_leaderboard_by_time_period(start_time)
    return leaderboard

@api_view(['GET'])
def weekly_leaderboard(request):
    leaderboard = get_leaderboard_by_time_frame(timedelta(weeks=1))
    if not leaderboard:
        return Response({"message": "No leaderboard data found for this time period."}, status=200)
    return Response(leaderboard)

@api_view(['GET'])
def monthly_leaderboard(request):
    leaderboard = get_leaderboard_by_time_frame(timedelta(days=30))
    if not leaderboard:
        return Response({"message": "No leaderboard data found for this time period."}, status=200)
    return Response(leaderboard)

@api_view(['GET'])
def yearly_leaderboard(request):
    leaderboard = get_leaderboard_by_time_frame(timedelta(days=365))
    if not leaderboard:
        return Response({"message": "No leaderboard data found for this time period."}, status=200)
    return Response(leaderboard)


# all time


def index(request):
    return HttpResponse("Leaderboard index page.")

@api_view(['GET'])
def leaderboard(request):
    users = CustomUser.objects.filter(is_admin=False).order_by('-experience_points')[:10]
    serializer = CustomUserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)

