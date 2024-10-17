from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, PointsLog, FriendList
from django.utils import timezone


class FriendsLeaderboardTests(APITestCase):

    def setUp(self):
        # clear all data
        CustomUser.objects.all().delete()
        PointsLog.objects.all().delete()
        FriendList.objects.all().delete()

        # create test user
        self.user1 = CustomUser.objects.create_user(username='user1', password='pass')
        self.user2 = CustomUser.objects.create_user(username='user2', password='pass')
        self.user3 = CustomUser.objects.create_user(username='user3', password='pass')

        # delete auto-created PointsLog
        PointsLog.objects.filter(user__in=[self.user1, self.user2, self.user3]).delete()

        # create friends
        FriendList.objects.create(user=self.user1)
        FriendList.objects.create(user=self.user2)
        FriendList.objects.create(user=self.user3)

        self.user1.friend_list.friends.add(self.user2)
        self.user2.friend_list.friends.add(self.user1)

        # create initial pointsLog
        now = timezone.now()
        PointsLog.objects.create(user=self.user1, experience_points=100, shop_points=50, created_at=now)
        PointsLog.objects.create(user=self.user2, experience_points=200, shop_points=80, created_at=now)
        PointsLog.objects.create(user=self.user3, experience_points=150, shop_points=60, created_at=now)

        # mock user login
        self.client.credentials(HTTP_AUTHORIZATION='Username ' + self.user1.username)

    def test_friends_leaderboard(self):
        url = reverse('friends_leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Print the leaderboard data
        print("Friends Leaderboard Data:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # The leaderboard should include user1 and user2 (friends)
        self.assertEqual(len(data), 2)
        usernames = [user['username'] for user in data]
        self.assertIn('user1', usernames)
        self.assertIn('user2', usernames)
        self.assertNotIn('user3', usernames)
