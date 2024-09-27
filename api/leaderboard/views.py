from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.serializers import CustomUserSerializer
from user.models import CustomUser, PointsLog


def get_user_id_from_request(request):
    # get user id from request
    user_id = request.headers.get('Authorization', '').split()[-1]
    return user_id

# get leaderboard by time, limit to top 10
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
    current_user_id = get_user_id_from_request(request)
    
    # if not in top 10
    current_user_in_top_10 = any(user['id'] == current_user_id for user in leaderboard)

    # if not in top 10, put in the tail
    if not current_user_in_top_10:
        current_user = CustomUser.objects.filter(id=current_user_id).first()
        if current_user:
            current_user_data = {
                'id': current_user.id,
                'username': current_user.username,
                'experience_points': current_user.experience_points,
                'shop_points': current_user.shop_points,
            }
            leaderboard.append(current_user_data)  # to the tail

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
    users = CustomUser.objects.filter(is_admin=False).order_by('-experience_points')[:10]  # top 10
    current_user_id = get_user_id_from_request(request)
    
    serializer = CustomUserSerializer(users, many=True, context={'request': request})
    users_data = serializer.data

    # if user in top 10
    current_user_in_top_10 = any(user['id'] == current_user_id for user in users_data)

    # if not in top 10, put in the tail
    if not current_user_in_top_10:
        current_user = CustomUser.objects.get(id=current_user_id)
        current_user_data = CustomUserSerializer(current_user, context={'request': request}).data
        users_data.append(current_user_data)  # put user to the tail

    return Response(users_data)

def index(request):
    return HttpResponse("Leaderboard index page.")
