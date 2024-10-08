from django.urls import path
from .views import get_quiz_questions, submit_quiz, finalize_quiz_score, check_quiz_eligibility, quiz_leaderboard

urlpatterns = [
    path('<int:quiz_id>/questions/', get_quiz_questions, name='get_quiz_questions'),
    path('<int:quiz_id>/submit/', submit_quiz, name='submit_quiz'),
    path('<int:quiz_id>/finalize/', finalize_quiz_score, name='finalize_quiz_score'),
    path('<int:quiz_id>/eligibility/', check_quiz_eligibility, name='check_quiz_eligibility'),
    path('<int:quiz_id>/leaderboard/', quiz_leaderboard, name='quiz_leaderboard'),
]
