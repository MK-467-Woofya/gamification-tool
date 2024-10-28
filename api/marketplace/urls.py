from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Register the ViewSets for each API object within the marketplace application
# Routes collected in gamification_tool main application.
router = DefaultRouter()
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'avatars', views.AvatarViewSet, basename='avatars')

urlpatterns = [
    path("", include(router.urls)),
]
