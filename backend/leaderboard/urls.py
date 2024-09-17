from django.urls import path
from .views import index, leaderboard

urlpatterns = [
    path('', index, name='index'),
    path('leaderboard/', leaderboard, name='leaderboard'),
]

