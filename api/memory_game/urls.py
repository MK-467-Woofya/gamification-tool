# memory_game/urls.py

from django.urls import path
from .views import submit_score

urlpatterns = [
    path('submit-score/', submit_score, name='submit_score'),
]
