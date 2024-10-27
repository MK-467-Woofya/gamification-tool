from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckInLocationViewSet

router = DefaultRouter()
router.register(r'checkins', CheckInLocationViewSet, basename='checkins')

urlpatterns = [
    path('', include(router.urls)),
]