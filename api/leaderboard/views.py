from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.serializers import CustomUserSerializer
from user.models import CustomUser, PointsLog

from rest_framework.exceptions import NotAuthenticated


def get_username_from_request(request):
    # get user name from request
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Username '):
        username = auth_header[len('Username '):]
        return username
    else:
        return None


# leaderboard in time period(top 10)
def get_leaderboard_by_time_period(start_time):
    logs = PointsLog.objects.filter(created_at__gte=start_time, user__is_admin=False) \
                            .select_related('user') \
                            .order_by('-experience_points')[:10]  # top 10

    user_scores = {}
    for log in logs:
        user_id = log.user.id
        if user_id not in user_scores or user_scores[user_id]['experience_points'] < log.experience_points:
            user_scores[user_id] = {
                'id': user_id,  # user id
                'username': log.user.username,
                'experience_points': log.experience_points,
                'shop_points': log.shop_points,
            }

    return sorted(user_scores.values(), key=lambda x: x['experience_points'], reverse=True)


def get_leaderboard_by_time_frame(time_delta, request):
    start_time = timezone.now() - time_delta
    leaderboard = get_leaderboard_by_time_period(start_time)  # top 10
    current_username = get_username_from_request(request)

    # if current user in top 10
    current_user_in_top_10 = any(user['username'] == current_username for user in leaderboard)

    # if not, add it into tail
    if not current_user_in_top_10 and current_username:
        current_user = CustomUser.objects.filter(username=current_username).first()
        if current_user:
            current_user_data = {
                'id': current_user.id,
                'username': current_user.username,
                'experience_points': current_user.experience_points,
                'shop_points': current_user.shop_points,
            }
            leaderboard.append(current_user_data)

    return leaderboard


@api_view(['GET'])
def weekly_leaderboard(request):
    leaderboard = get_leaderboard_by_time_frame(timedelta(weeks=1), request)
    return Response(leaderboard)


@api_view(['GET'])
def monthly_leaderboard(request):
    leaderboard = get_leaderboard_by_time_frame(timedelta(days=30), request)
    return Response(leaderboard)


@api_view(['GET'])
def yearly_leaderboard(request):
    leaderboard = get_leaderboard_by_time_frame(timedelta(days=365), request)
    return Response(leaderboard)


@api_view(['GET'])
def leaderboard(request):
    users = CustomUser.objects.filter(is_admin=False).order_by('-experience_points')[:10]
    current_username = get_username_from_request(request)

    serializer = CustomUserSerializer(users, many=True, context={'request': request})
    users_data = serializer.data

    # if current user in top 10
    current_user_in_top_10 = any(user['username'] == current_username for user in users_data)

    # if not
    if not current_user_in_top_10 and current_username:
        current_user = CustomUser.objects.filter(username=current_username).first()
        if current_user:
            current_user_data = CustomUserSerializer(current_user, context={'request': request}).data
            users_data.append(current_user_data)

    return Response(users_data)


def index(request):
    return HttpResponse("Leaderboard index page.")


@api_view(['GET'])
def friends_leaderboard(request):
    # current user
    current_username = get_username_from_request(request)
    current_user = CustomUser.objects.filter(username=current_username).first()

    if not current_user:
        return Response({"error": "User not found"}, status=404)

    # friend list
    friends = current_user.friend_list.friends.all()

    # friend and current user
    friends_and_self_logs = PointsLog.objects.filter(user__in=[*friends, current_user]).select_related('user').order_by('-experience_points')

    leaderboard = []
    for log in friends_and_self_logs:
        leaderboard.append({
            'username': log.user.username,
            'experience_points': log.experience_points,
            'shop_points': log.shop_points,
            'is_current_user': log.user == current_user
        })

    return Response(leaderboard)
