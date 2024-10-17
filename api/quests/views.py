from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Quest, UserQuestProgress
from .serializers import QuestSerializer, UserQuestProgressSerializer

class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Optionally, add logic to automatically assign quests to users when a quest is created
        serializer.save()

class UserQuestProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserQuestProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return the quest progress for the currently authenticated user
        return UserQuestProgress.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        quest_progress = serializer.save()
        # Check if the user has completed the quest
        if quest_progress.progress >= quest_progress.quest.goal:
            quest_progress.completed = True
            quest_progress.save()
            # Optionally: Automatically reward points when the quest is completed
            if not quest_progress.rewards_claimed:
                # Call your reward logic here
                quest_progress.rewards_claimed = True
                quest_progress.save()