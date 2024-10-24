from rest_framework import viewsets
from .models import Quest, UserQuestProgress
from .serializers import QuestSerializer, UserQuestProgressSerializer
from rest_framework.response import Response
from rest_framework import status

class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer

    def perform_create(self, serializer):
        # Optionally, add logic to automatically assign quests to users when a quest is created
        serializer.save()

class UserQuestProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserQuestProgressSerializer

    def get_queryset(self):
        # Always return all user progress, as the request is never tied to an authenticated user
        return UserQuestProgress.objects.all()

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

    def retrieve(self, request, *args, **kwargs):
        """Override the retrieve method for API key-only access"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)