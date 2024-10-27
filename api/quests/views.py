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
        if self.action == 'list':
            current_date = timezone.now()
            user_id = self.request.query_params.get('user_id', None)
            if user_id is None:
                return UserQuestProgress.objects.none()
            active_quests = Quest.objects.filter(start_date__lte=current_date, end_date__gte=current_date)
            return UserQuestProgress.objects.filter(user_id=user_id, quest__in=active_quests)
        return UserQuestProgress.objects.all()

    def perform_update(self, serializer):
        quest_progress = serializer.save()

        # Check if the progress meets or exceeds the goal to mark as complete
        if quest_progress.progress >= quest_progress.quest.goal and not quest_progress.completed:
            quest_progress.completed = True
            quest_progress.save()

            # Check if rewards have not been claimed and mark as claimed
            if not quest_progress.rewards_claimed:
                quest_progress.rewards_claimed = True
                quest_progress.save()

                # Add rewards to the user's account
                user = quest_progress.user
                user.experience_points += quest_progress.quest.rewards
                user.shop_points += quest_progress.quest.rewards
                user.save()  # Save the user's updated points

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = UserQuestProgress.objects.get(pk=kwargs['pk'])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except UserQuestProgress.DoesNotExist:
            raise NotFound("No UserQuestProgress matches the given query.")