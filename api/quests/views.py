from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Quest, UserQuestProgress
from .serializers import QuestSerializer, UserQuestProgressSerializer
from user.models import CustomUser
from django.utils import timezone

class QuestViewSet(viewsets.ModelViewSet):
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer

    def perform_create(self, serializer):
        new_quest = serializer.save()
        users = CustomUser.objects.all()
        for user in users:
            UserQuestProgress.objects.create(
                user=user,
                quest=new_quest,
                progress=0,
                completed=False,
                rewards_claimed=False
            )

    def perform_destroy(self, instance):
        UserQuestProgress.objects.filter(quest=instance).delete()
        instance.delete()

class UserQuestProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserQuestProgressSerializer
    lookup_field = 'pk'  # Use primary key lookup for retrieve and update

    def get_queryset(self):
        # Only filter for list action, showing active quests for the logged-in user
        if self.action == 'list':
            current_date = timezone.now()
            user_id = self.request.query_params.get('user_id', None)
            
            if user_id is None:
                return UserQuestProgress.objects.none()

            # Filter active quests based on the current date
            active_quests = Quest.objects.filter(start_date__lte=current_date, end_date__gte=current_date)

            # Filter UserQuestProgress for the specified user and active quests
            return UserQuestProgress.objects.filter(user_id=user_id, quest__in=active_quests)
        
        # For retrieve, update, partial_update, we allow full access to primary keys
        return UserQuestProgress.objects.all()

    def perform_update(self, serializer):
        quest_progress = serializer.save()
        
        # Check if the progress meets or exceeds the goal to mark as complete
        if quest_progress.progress >= quest_progress.quest.goal:
            quest_progress.completed = True
            quest_progress.save()

            # Mark rewards as claimed if quest is completed
            if not quest_progress.rewards_claimed:
                quest_progress.rewards_claimed = True
                quest_progress.save()

    def retrieve(self, request, *args, **kwargs):
        """Retrieve UserQuestProgress by its primary key without filtering by user or active quests"""
        try:
            instance = UserQuestProgress.objects.get(pk=kwargs['pk'])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except UserQuestProgress.DoesNotExist:
            raise NotFound("No UserQuestProgress matches the given query.")