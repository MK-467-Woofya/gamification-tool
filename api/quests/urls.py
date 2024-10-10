from rest_framework.routers import DefaultRouter
from .views import QuestViewSet

router = DefaultRouter()
router.register(r'quests', QuestViewSet, basename='quest')

urlpatterns = router.urls