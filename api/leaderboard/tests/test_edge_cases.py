from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, PointsLog
from datetime import timedelta
from django.utils import timezone


class LeaderboardEdgeCasesTests(APITestCase):

    def setUp(self):
        # clear all data
        CustomUser.objects.all().delete()
        PointsLog.objects.all().delete()

        # create test user
        self.user1 = CustomUser.objects.create_user(username='user1', password='pass')
        self.user2 = CustomUser.objects.create_user(username='user2', password='pass')

        # delete auto-created PointsLog
        PointsLog.objects.filter(user__in=[self.user1, self.user2]).delete()

        # create initial pointsLog 
        now = timezone.now()
        PointsLog.objects.create(user=self.user1, experience_points=100, shop_points=50, created_at=now)
        PointsLog.objects.create(user=self.user2, experience_points=200, shop_points=80, created_at=now)

        # mock user login
        self.client.credentials(HTTP_AUTHORIZATION='Username ' + self.user1.username)


    
    def test_leaderboard_no_pointslog_entries(self):
        # Delete all PointsLog entries
        PointsLog.objects.all().delete()

        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # The leaderboard should be empty
        self.assertEqual(len(data), 0)

    
    def test_leaderboard_with_negative_scores(self):
        # PointsLog with negative score
        PointsLog.objects.create(user=self.user1, experience_points=-50, shop_points=25)

        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # output leaderboard
        print("Leaderboard Data with Negative Scores:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # check the correctness of user score
        user1_data = next((user for user in data if user['username'] == 'user1'), None)
        self.assertIsNotNone(user1_data)
        expected_total_points = 100 - 50  # initial 100 plus -50
        self.assertEqual(user1_data['experience_points'], expected_total_points)



    def test_leaderboard_with_tie_scores(self):
        # multiple user with same score
        PointsLog.objects.filter(user__in=[self.user1, self.user2]).delete()
        PointsLog.objects.create(user=self.user1, experience_points=300, shop_points=50)
        PointsLog.objects.create(user=self.user2, experience_points=300, shop_points=50)

        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # leaderboard
        print("Leaderboard Data with Tie Scores:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # check the rank
        user1_data = next((user for user in data if user['username'] == 'user1'), None)
        user2_data = next((user for user in data if user['username'] == 'user2'), None)
        self.assertIsNotNone(user1_data)
        self.assertIsNotNone(user2_data)
        self.assertEqual(user1_data['rank'], user2_data['rank'])


    def test_leaderboard_with_boundary_dates(self):
        # create a pointsLog with time 7 days plus 1 second ago
        boundary_date = timezone.now() - timedelta(days=7) + timedelta(seconds=1)
        PointsLog.objects.create(user=self.user1, experience_points=50, shop_points=25, created_at=boundary_date)

        url = reverse('weekly_leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # leaderboard
        print("Weekly Leaderboard Data with Boundary Date:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # if user in the leaderboard
        usernames = [user['username'] for user in data]
        self.assertIn('user1', usernames)



    def test_leaderboard_with_large_dataset(self):
        # create 300 user and logs
        num_users = 300
        for i in range(4, num_users + 4):
            user = CustomUser.objects.create_user(username=f'user{i}', password='pass')
            PointsLog.objects.filter(user=user).delete()
            PointsLog.objects.create(user=user, experience_points=i, shop_points=50)

        url = reverse('leaderboard')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # output top 10
        print("Leaderboard Data with Large Dataset:")
        for user in data:
            print(f"Rank {user['rank']}: {user['username']} (Points: {user['experience_points']})")

        # check leaderboard includes top 10 and currfent user
        self.assertEqual(len(data), 11)




