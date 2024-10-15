from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, PointsLog, FriendList
from datetime import timedelta
from django.utils import timezone
from django.test.utils import override_settings

@override_settings(REST_FRAMEWORK={
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
})
class LeaderboardTests(APITestCase):

    def setUp(self):
        # clear all data
        CustomUser.objects.all().delete()
        PointsLog.objects.all().delete()
        FriendList.objects.all().delete()

        # test user
        self.user1 = CustomUser.objects.create_user(username='user1', password='pass')
        self.user2 = CustomUser.objects.create_user(username='user2', password='pass')
        self.user3 = CustomUser.objects.create_user(username='user3', password='pass')

        # delete auto created PointsLog
        PointsLog.objects.filter(user__in=[self.user1, self.user2, self.user3]).delete()

        # create friends
        FriendList.objects.create(user=self.user1)
        FriendList.objects.create(user=self.user2)
        FriendList.objects.create(user=self.user3)

        self.user1.friend_list.friends.add(self.user2)
        self.user2.friend_list.friends.add(self.user1)

        # points log
        now = timezone.now()
        PointsLog.objects.create(user=self.user1, experience_points=100, shop_points=50, created_at=now - timedelta(days=5))
        PointsLog.objects.create(user=self.user2, experience_points=200, shop_points=80, created_at=now - timedelta(days=6))
        PointsLog.objects.create(user=self.user3, experience_points=150, shop_points=60, created_at=now - timedelta(days=8))  # over a week

        # moke login
        self.client.credentials(HTTP_AUTHORIZATION='Username ' + self.user1.username)

    def test_weekly_leaderboard(self):
        url = reverse('weekly_leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # leaderboard data
        print("Weekly Leaderboard Data:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        self.assertEqual(len(data), 2)  # only user1 and user2 in 1 week
        usernames = [user['username'] for user in data]
        self.assertIn('user1', usernames)
        self.assertIn('user2', usernames)
        self.assertNotIn('user3', usernames)

    def test_current_user_not_in_top_10(self):
        # delete point log of user1
        PointsLog.objects.filter(user=self.user1).delete()

        # new log
        PointsLog.objects.create(user=self.user1, experience_points=10, shop_points=50)

        # create more user to let user1 out of top 10 
        for i in range(4, 15):
            user = CustomUser.objects.create_user(username=f'user{i}', password='pass')
            #  delete auto created PointsLog
            PointsLog.objects.filter(user=user).delete()
            PointsLog.objects.create(user=user, experience_points=500 + i, shop_points=50)

        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # leaderboard data
        print("Leaderboard Data:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        self.assertEqual(len(data), 11)  # top 10 and current user
        usernames = [user['username'] for user in data]
        self.assertIn('user1', usernames)
        self.assertTrue(any(user['is_current_user'] for user in data if user['username'] == 'user1'))

        # make sure user1 is top 11
        user1_data = next((user for user in data if user['username'] == 'user1'), None)
        self.assertIsNotNone(user1_data)
        self.assertGreaterEqual(user1_data['rank'], 11)
