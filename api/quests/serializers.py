from rest_framework import serializers
from .models import Quest, UserQuestProgress

class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = ['id', 'title', 'goal', 'start_date', 'end_date', 'rewards', 'description']

class UserQuestProgressSerializer(serializers.ModelSerializer):
    quest = QuestSerializer(read_only=True)

    class Meta:
        model = UserQuestProgress
        fields = ['id', 'user', 'quest', 'progress', 'completed', 'rewards_claimed']
        read_only_fields = ['user', 'quest', 'completed', 'rewards_claimed']