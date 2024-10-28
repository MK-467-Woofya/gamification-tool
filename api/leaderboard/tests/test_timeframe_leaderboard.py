from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, PointsLog
from datetime import timedelta
from django.utils import timezone


class TimeframeLeaderboardTests(APITestCase):

    def setUp(self):
        # clear all data
        CustomUser.objects.all().delete()
        PointsLog.objects.all().delete()

        # create test user
        self.user1 = CustomUser.objects.create_user(username='user1', password='pass')
        self.user2 = CustomUser.objects.create_user(username='user2', password='pass')
        self.user3 = CustomUser.objects.create_user(username='user3', password='pass')

        # delete auto-created PointsLog
        PointsLog.objects.filter(user__in=[self.user1, self.user2, self.user3]).delete()

        # create initial pointsLog
        now = timezone.now()
        PointsLog.objects.create(user=self.user1, experience_points=100, shop_points=50, created_at=now - timedelta(days=5))
        PointsLog.objects.create(user=self.user2, experience_points=200, shop_points=80, created_at=now - timedelta(days=6))
        PointsLog.objects.create(user=self.user3, experience_points=150, shop_points=60, created_at=now - timedelta(days=8))  # over 1 week

        # mock user login
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

    def test_monthly_leaderboard(self):
        url = reverse('monthly_leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Print the leaderboard data
        print("Monthly Leaderboard Data:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # All users have PointsLog entries within the last 30 days
        self.assertEqual(len(data), 3)  # All three users
        usernames = [user['username'] for user in data]
        self.assertIn('user1', usernames)
        self.assertIn('user2', usernames)
        self.assertIn('user3', usernames)

    def test_yearly_leaderboard(self):
        url = reverse('yearly_leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Print the leaderboard data
        print("Yearly Leaderboard Data:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # All users have PointsLog entries within the last year
        self.assertEqual(len(data), 3)  # All three users
        usernames = [user['username'] for user in data]
        self.assertIn('user1', usernames)
        self.assertIn('user2', usernames)
        self.assertIn('user3', usernames)
