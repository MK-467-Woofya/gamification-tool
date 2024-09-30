from django.urls import path

from .views import index, leaderboard, weekly_leaderboard, monthly_leaderboard, yearly_leaderboard

urlpatterns = [
    path('', index, name='index'),
    path('weekly/', weekly_leaderboard, name='weekly_leaderboard'),
    path('monthly/', monthly_leaderboard, name='monthly_leaderboard'),
    path('yearly/', yearly_leaderboard, name='yearly_leaderboard'),
    path('alltime/', leaderboard, name='leaderboard'),  # total

]
