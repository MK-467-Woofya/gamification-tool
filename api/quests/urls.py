from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestViewSet, UserQuestProgressViewSet

router = DefaultRouter()
router.register(r'quests', QuestViewSet)
router.register(r'user-progress', UserQuestProgressViewSet, basename='userquestprogress')

urlpatterns = router.urls + [
    # Explicitly define a retrieve path
    path('user-progress/<int:pk>/', UserQuestProgressViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
]