from rest_framework.routers import DefaultRouter
from .views import QuestViewSet, UserQuestProgressViewSet

router = DefaultRouter()
router.register(r'quests', QuestViewSet)
router.register(r'user-progress', UserQuestProgressViewSet, basename='userquestprogress')

urlpatterns = router.urls