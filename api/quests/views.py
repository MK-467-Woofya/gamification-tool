from rest_framework import viewsets
from .models import Quest, UserQuestProgress
from .serializers import QuestSerializer, UserQuestProgressSerializer  # Add the missing import
from user.models import CustomUser  # Import the CustomUser model
from django.utils import timezone

class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer

    def perform_create(self, serializer):
        # Create the quest first
        new_quest = serializer.save()

        # Fetch all users from CustomUser
        users = CustomUser.objects.all()

        # Create a UserQuestProgress entry for each user
        for user in users:
            UserQuestProgress.objects.create(
                user=user,
                quest=new_quest,
                progress=0,
                completed=False,
                rewards_claimed=False
            )

    def perform_destroy(self, instance):
        # When a quest is deleted, also delete all related UserQuestProgress
        UserQuestProgress.objects.filter(quest=instance).delete()
        # Now delete the quest itself
        instance.delete()

class UserQuestProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserQuestProgressSerializer

    def get_queryset(self):
        # Get the current date
        current_date = timezone.now()

        # Get user ID from the request query parameters
        user_id = self.request.query_params.get('user_id', None)

        if user_id is None:
            return UserQuestProgress.objects.none()  # Return empty queryset if no user_id is provided

        # Filter quests that are currently active (start_date <= current_date <= end_date)
        active_quests = Quest.objects.filter(start_date__lte=current_date, end_date__gte=current_date)

        # Filter UserQuestProgress for the given user and active quests
        return UserQuestProgress.objects.filter(user_id=user_id, quest__in=active_quests)

    def perform_update(self, serializer):
        quest_progress = serializer.save()
        # Check if the user has completed the quest
        if quest_progress.progress >= quest_progress.quest.goal:
            quest_progress.completed = True
            quest_progress.save()

            # Optionally: Automatically reward points when the quest is completed
            if not quest_progress.rewards_claimed:
                quest_progress.rewards_claimed = True
                quest_progress.save()

    def retrieve(self, request, *args, **kwargs):
        """Override the retrieve method for API key-only access"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)