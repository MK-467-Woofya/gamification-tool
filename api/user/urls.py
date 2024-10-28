from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Register the ViewSets for each API object within the users application
# Routes collected in gamification_tool main application.
router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='users')

urlpatterns = [
    path("", include(router.urls)),  # /user
]

# leaderboard - no need this part because @action in views.py/CustomerUserViewSet will create path for it
# urlpatterns += [
#     path('leaderboard/', views.CustomerUserViewSet.as_view({'get': 'leaderboard'}), name='leaderboard')
# ]
