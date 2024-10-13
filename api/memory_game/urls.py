# memory_game/urls.py

from django.urls import path
from .views import submit_score, check_game_eligibility, memory_game_leaderboard

urlpatterns = [
    path('submit-score/', submit_score, name='submit_score'),
    path('eligibility/', check_game_eligibility, name='check_game_eligibility'),
    path('leaderboard/', memory_game_leaderboard, name='memory_game_leaderboard'),
]
