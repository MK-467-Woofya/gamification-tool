from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import CustomUser, PointsLog

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny


def get_username_from_request(request):
    # Get user name from request
    # auth_header = request.headers.get('Authorization', '')
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header.startswith('Username '):
        username = auth_header[len('Username '):]
        return username
    else:
        return None

def get_leaderboard_by_time_frame(time_delta, request):
    # If time_delta is None, calculate leaderboard for all time
    if time_delta is not None:
        start_time = timezone.now() - time_delta
        print(f"Calculating leaderboard with start_time >= {start_time}")
        logs = PointsLog.objects.filter(
            created_at__gte=start_time
        ).exclude(user__is_superuser=True).select_related('user')
    else:
        logs = PointsLog.objects.all().exclude(
            user__is_superuser=True
        ).select_related('user')

    print(f"Found {logs.count()} PointsLog entries")

    user_scores = {}
    for log in logs:
        user_id = log.user.id
        if user_id not in user_scores:
            user_scores[user_id] = {
                'id': user_id,  # user id
                'username': log.user.username,
                'experience_points': log.experience_points,
                'shop_points': log.shop_points,
            }
        else:
            # Accumulate experience_points and shop_points
            user_scores[user_id]['experience_points'] += log.experience_points
            user_scores[user_id]['shop_points'] += log.shop_points

    # Sort the leaderboard
    leaderboard_list = sorted(user_scores.values(), key=lambda x: x['experience_points'], reverse=True)

    current_username = get_username_from_request(request)
    print(f"Current user: {current_username}")

    # Add rank and is_current_user fields with handling ties
    leaderboard = []
    previous_score = None
    rank = 0
    for i, user_data in enumerate(leaderboard_list):
        if user_data['experience_points'] != previous_score:
            rank = i + 1
            previous_score = user_data['experience_points']
        user_data['rank'] = rank
        user_data['is_current_user'] = (user_data['username'] == current_username)
        leaderboard.append(user_data)

    # Get top 10 users
    top_10_leaderboard = leaderboard_list[:10]

    # Check if current user is in the top 10
    current_user_in_top_10 = any(
        user['username'] == current_username for user in top_10_leaderboard
    )

    # If current user is not in top 10 and is logged in, add them to the leaderboard
    if not current_user_in_top_10 and current_username:
        current_user_data = next(
            (user for user in leaderboard_list if user['username'] == current_username), None
        )
        if current_user_data:
            top_10_leaderboard.append(current_user_data)

    print(f"Top 10 leaderboard: {top_10_leaderboard}")

    return top_10_leaderboard  # Return top 10 users and current user's data

@api_view(['GET'])
@permission_classes([AllowAny])
def weekly_leaderboard(request):
    leaderboard = get_leaderboard_by_time_frame(timedelta(weeks=1), request)
    return Response(leaderboard)

@api_view(['GET'])
@permission_classes([AllowAny])
def monthly_leaderboard(request):
    leaderboard = get_leaderboard_by_time_frame(timedelta(days=30), request)
    return Response(leaderboard)

@api_view(['GET'])
@permission_classes([AllowAny])
def yearly_leaderboard(request):
    leaderboard = get_leaderboard_by_time_frame(timedelta(days=365), request)
    return Response(leaderboard)

@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    # For all-time leaderboard, pass time_delta as None
    leaderboard = get_leaderboard_by_time_frame(None, request)
    return Response(leaderboard)

@permission_classes([AllowAny])
def index(request):
    return HttpResponse("Leaderboard index page.")

@api_view(['GET'])
@permission_classes([AllowAny])
def friends_leaderboard(request):
    # current user
    current_username = get_username_from_request(request)
    current_user = CustomUser.objects.filter(username=current_username).first()

    if not current_user:
        return Response({"error": "User not found"}, status=404)

    # friend list
    friends = current_user.friend_list.friends.all()

    # logs for friends and current user
    friends_and_self_logs = PointsLog.objects.filter(
        user__in=[*friends, current_user]
    ).select_related('user')

    user_scores = {}
    for log in friends_and_self_logs:
        user_id = log.user.id
        if user_id not in user_scores:
            user_scores[user_id] = {
                'username': log.user.username,
                'experience_points': log.experience_points,
                'shop_points': log.shop_points,
                'is_current_user': (log.user.username == current_username)
            }
        else:
            # Accumulate experience_points and shop_points
            user_scores[user_id]['experience_points'] += log.experience_points
            user_scores[user_id]['shop_points'] += log.shop_points

    # Sort leaderboard
    leaderboard_list = sorted(
        user_scores.values(), key=lambda x: x['experience_points'], reverse=True
    )

    # Add rank
    for index, user_data in enumerate(leaderboard_list):
        user_data['rank'] = index + 1  # Rank starts from 1

    return Response(leaderboard_list)
