from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# register the ViewSets with for each API objct type
router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='users')

urlpatterns = [
    path("", include(router.urls)), # /user
]