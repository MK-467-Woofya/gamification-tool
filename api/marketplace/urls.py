from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# register the ViewSets with for each API objct type
router = DefaultRouter()
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(r'avatars', views.AvatarViewSet, basename='avatars')

urlpatterns = [
    path("", include(router.urls)),
]
