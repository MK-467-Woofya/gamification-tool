from django.urls import path

from . import views
"""
URL patterns for the check_in views.
These are included in the main project gamification/urls.py
"""
app_name = "check_in"
urlpatterns = [
    # /check_in/
    path("", views.IndexView.as_view(), name="index"),
    # /check_in/1/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # /check_in/1/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # /check_in/1/visit_event/ --- Non-generic view URL
    path("<int:location_id>/visit_event/", views.visit_event, name="visit_event")
]
