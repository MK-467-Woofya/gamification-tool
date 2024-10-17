from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Quest
from .serializers import QuestSerializer

class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Set the user to the logged-in user when a quest is created
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Only return quests for the currently authenticated user
        return Quest.objects.filter(user=self.request.user)