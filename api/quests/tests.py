#These tests may not work
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Quest, UserQuestProgress

class QuestModelTest(TestCase):

    def test_create_quest(self):
        quest = Quest.objects.create(
            title="Walk 10km",
            goal=10,
            start_date="2024-07-01",
            end_date="2024-07-31",
            rewards="100 XP"
        )
        self.assertEqual(quest.title, "Walk 10km")
        self.assertEqual(quest.goal, 10)

class UserQuestProgressTest(TestCase):

    def test_create_user_quest_progress(self):
        user = get_user_model().objects.create(username='testuser')
        quest = Quest.objects.create(
            title="Walk 10km",
            goal=10,
            start_date="2024-07-01",
            end_date="2024-07-31",
            rewards="100 XP"
        )
        progress = UserQuestProgress.objects.create(
            user=user,
            quest=quest,
            progress=5.0
        )
        self.assertEqual(progress.progress, 5.0)
        self.assertFalse(progress.completed)