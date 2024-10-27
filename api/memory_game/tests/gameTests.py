from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, PointsLog, update_user_points
from memory_game.models import UserMemoryGameScore
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

class TestMemoryGame(APITestCase):
    def setUp(self):
        # create test user
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')
        self.user2 = CustomUser.objects.create_user(username='testuser2', password='testpass')
    
    def test_submit_score_success(self):
        url = reverse('submit_score')
        data = {
            'username': 'testuser',
            'score': 50
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Game completed. Your score has been recorded.')
        
        # if UserMemoryGameScore created
        self.assertTrue(UserMemoryGameScore.objects.filter(user=self.user, score=50, eligible_for_leaderboard=True).exists())
        
        # if experience_points updated
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.experience_points, 50)
        
        # if PointsLog recorded
        points_log = PointsLog.objects.filter(user=self.user).aggregate(total_experience_points=Sum('experience_points'))
        self.assertEqual(points_log['total_experience_points'], 50)
    
    def test_submit_score_within_cooldown(self):
        # create a record in 2 days ago
        UserMemoryGameScore.objects.create(user=self.user, score=30, eligible_for_leaderboard=True, completed_at=timezone.now() - timedelta(days=2))
        update_user_points(self.user, 30, 0)
        
        url = reverse('submit_score')
        data = {
            'username': 'testuser',
            'score': 20
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Game completed. You did not earn points this time.')
        
        # if UserMemoryGameScore created
        self.assertTrue(UserMemoryGameScore.objects.filter(user=self.user, score=20, eligible_for_leaderboard=False).exists())
        
        # if experience_points increased
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.experience_points, 30)  # only 30 score
    
    def test_submit_score_after_cooldown(self):
        # create a record after cooldown(4 days ago)
        score_record = UserMemoryGameScore.objects.create(
            user=self.user,
            score=30,
            eligible_for_leaderboard=True
        )
        # update completed_at to 4 days ago
        UserMemoryGameScore.objects.filter(pk=score_record.pk).update(
            completed_at=timezone.now() - timedelta(days=4)
        )
        # get record again
        score_record.refresh_from_db()
        
        # if completed_at set correctly
        self.assertGreaterEqual(timezone.now() - score_record.completed_at, timedelta(days=4))
        
        update_user_points(self.user, 30, 0)
        
        url = reverse('submit_score')
        data = {
            'username': 'testuser',
            'score': 20
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Game completed. Your score has been recorded.')
        
        # if UserMemoryGameScore created
        self.assertTrue(UserMemoryGameScore.objects.filter(user=self.user, score=20, eligible_for_leaderboard=True).exists())
        
        # if experience_points increased
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.experience_points, 50)  # 30 + 20

    
    def test_submit_score_missing_fields(self):
        url = reverse('submit_score')
        data = {
            'username': 'testuser',
            # lack 'score'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_submit_score_invalid_score(self):
        url = reverse('submit_score')
        data = {
            'username': 'testuser',
            'score': 'invalid_score'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_submit_score_nonexistent_user(self):
        url = reverse('submit_score')
        data = {
            'username': 'nonexistentuser',
            'score': 20
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
    
    def test_check_game_eligibility_first_time(self):
        url = reverse('check_game_eligibility')
        # mock user authorize
        self.client.credentials(HTTP_AUTHORIZATION='Username ' + self.user.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['eligible'])
        self.assertTrue(response.data['can_earn_points'])
    
    def test_check_game_eligibility_within_cooldown(self):
        # create a record in 2 days ago
        UserMemoryGameScore.objects.create(user=self.user, score=30, eligible_for_leaderboard=True, completed_at=timezone.now() - timedelta(days=2))
        update_user_points(self.user, 30, 0)
        
        url = reverse('check_game_eligibility')
        # mock user authorize
        self.client.credentials(HTTP_AUTHORIZATION='Username ' + self.user.username)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['eligible'])
        self.assertFalse(response.data['can_earn_points'])
        self.assertIn('remaining_time', response.data)
        self.assertIn('hours', response.data['remaining_time'])
        self.assertIn('minutes', response.data['remaining_time'])
        self.assertIn('seconds', response.data['remaining_time'])
    
    def test_check_game_eligibility_after_cooldown(self):
        # create a record after cooldown(4 days ago)
        score_record = UserMemoryGameScore.objects.create(
            user=self.user,
            score=30,
            eligible_for_leaderboard=True
        )
        # update completed_at to 4 days ago
        UserMemoryGameScore.objects.filter(pk=score_record.pk).update(
            completed_at=timezone.now() - timedelta(days=4)
        )
        # get record again
        score_record.refresh_from_db()
        
        # if completed_at set correctly
        self.assertGreaterEqual(timezone.now() - score_record.completed_at, timedelta(days=4))
        
        url = reverse('check_game_eligibility')
        # mock user authorize
        self.client.credentials(HTTP_AUTHORIZATION='Username ' + self.user.username)
        response = self.client.get(url)
        
        # confirm completed_at and time_since_last_play
        last_score = UserMemoryGameScore.objects.filter(user=self.user).order_by('-completed_at').first()
        self.assertIsNotNone(last_score)
        self.assertEqual(last_score.completed_at, score_record.completed_at)
        time_since_last_play = timezone.now() - last_score.completed_at
        self.assertGreaterEqual(time_since_last_play, timedelta(days=4))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['eligible'])
        self.assertTrue(response.data['can_earn_points'])
        self.assertNotIn('remaining_time', response.data)

    
    def test_check_game_eligibility_unauthorized(self):
        url = reverse('check_game_eligibility')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_memory_game_leaderboard_success(self):
        # create record able to on leaderboard
        UserMemoryGameScore.objects.create(user=self.user, score=50, eligible_for_leaderboard=True, completed_at=timezone.now() - timedelta(days=4))
        UserMemoryGameScore.objects.create(user=self.user2, score=40, eligible_for_leaderboard=True, completed_at=timezone.now() - timedelta(days=4))
        update_user_points(self.user, 50, 0)
        update_user_points(self.user2, 40, 0)
        
        url = reverse('memory_game_leaderboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], 'testuser')
        self.assertEqual(response.data[0]['total_score'], 50)
        self.assertEqual(response.data[1]['username'], 'testuser2')
        self.assertEqual(response.data[1]['total_score'], 40)
    
    def test_memory_game_leaderboard_no_scores(self):
        url = reverse('memory_game_leaderboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)
    
    def test_memory_game_leaderboard_partial_scores(self):
        # create record able and not able to be on leaderboard
        UserMemoryGameScore.objects.create(user=self.user, score=50, eligible_for_leaderboard=True, completed_at=timezone.now() - timedelta(days=4))
        UserMemoryGameScore.objects.create(user=self.user2, score=40, eligible_for_leaderboard=False, completed_at=timezone.now() - timedelta(days=4))
        update_user_points(self.user, 50, 0)
        update_user_points(self.user2, 40, 0)
        
        url = reverse('memory_game_leaderboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')
        self.assertEqual(response.data[0]['total_score'], 50)
