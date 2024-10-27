from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, PointsLog
from django.utils import timezone


class LeaderboardTests(APITestCase):

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
        PointsLog.objects.create(user=self.user1, experience_points=100, shop_points=50, created_at=timezone.now())
        PointsLog.objects.create(user=self.user2, experience_points=200, shop_points=80, created_at=timezone.now())
        PointsLog.objects.create(user=self.user3, experience_points=150, shop_points=60, created_at=timezone.now())

        # mock user login
        self.client.credentials(HTTP_AUTHORIZATION='Username ' + self.user1.username)

    def test_all_time_leaderboard(self):
        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Print the leaderboard data
        print("All-Time Leaderboard Data:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # All users should be present
        self.assertEqual(len(data), 3)
        usernames = [user['username'] for user in data]
        self.assertIn('user1', usernames)
        self.assertIn('user2', usernames)
        self.assertIn('user3', usernames)

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

    def test_current_user_in_top_10(self):
        # Ensure user1 has high enough points
        PointsLog.objects.filter(user=self.user1).delete()
        PointsLog.objects.create(user=self.user1, experience_points=1000, shop_points=50)

        # Create additional users with lower points
        for i in range(4, 15):
            user = CustomUser.objects.create_user(username=f'user{i}', password='pass')
            # Delete auto-created PointsLog
            PointsLog.objects.filter(user=user).delete()
            PointsLog.objects.create(user=user, experience_points=100 + i, shop_points=50)

        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Print the leaderboard data
        print("Leaderboard Data with Current User in Top 10:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # The leaderboard should contain only the top 10 users
        self.assertEqual(len(data), 10)
        usernames = [user['username'] for user in data]
        self.assertIn('user1', usernames)
        self.assertTrue(any(user['is_current_user'] for user in data if user['username'] == 'user1'))

    def test_points_accumulation(self):
        # Add additional PointsLog entries for user1
        PointsLog.objects.create(user=self.user1, experience_points=50, shop_points=25)
        PointsLog.objects.create(user=self.user1, experience_points=25, shop_points=10)

        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Print the leaderboard data
        print("Leaderboard Data with Points Accumulation:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # Calculate expected total points for user1
        expected_total_points = 100 + 50 + 25  # From initial setup and the two new entries

        # Find user1's data
        user1_data = next((user for user in data if user['username'] == 'user1'), None)
        self.assertIsNotNone(user1_data)
        self.assertEqual(user1_data['experience_points'], expected_total_points)

    def test_is_current_user_flag(self):
        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Print the leaderboard data
        print("Leaderboard Data for is_current_user Flag Test:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (is_current_user: {user['is_current_user']})")

        # Check that 'is_current_user' is True only for the current user
        for user in data:
            if user['username'] == self.user1.username:
                self.assertTrue(user['is_current_user'])
            else:
                self.assertFalse(user.get('is_current_user', False))

    def test_leaderboard_without_login(self):
        # Remove the credentials to simulate not logged in
        self.client.credentials()

        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Print the leaderboard data
        print("Leaderboard Data without Login:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # The leaderboard should contain only the top 10 users
        # Since current user is not logged in, 'is_current_user' should not be True for any user
        for user in data:
            self.assertFalse(user.get('is_current_user', False))

    def test_leaderboard_with_invalid_user(self):
        # Set invalid username in the credentials
        self.client.credentials(HTTP_AUTHORIZATION='Username invalid_user')

        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Print the leaderboard data
        print("Leaderboard Data with Invalid User:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # The leaderboard should contain only the top 10 users
        # Since current user does not exist, 'is_current_user' should not be True for any user
        for user in data:
            self.assertFalse(user.get('is_current_user', False))
