# quiz/tests/test_quiz.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser, PointsLog
from quiz.models import Quiz, QuizQuestion, QuizChoice, UserQuizScore
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

class QuizAPITests(APITestCase):

    def setUp(self):
        # create user
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')
        self.user2 = CustomUser.objects.create_user(username='testuser2', password='testpass')

        # create quiz
        self.quiz = Quiz.objects.create(name='General Knowledge Quiz')

        # create question
        self.question1 = QuizQuestion.objects.create(
            quiz=self.quiz,
            question_text='What is the capital of France?',
            correct_answer='Paris',
            points=10
        )
        self.choice1_q1 = QuizChoice.objects.create(
            question=self.question1,
            text='Paris'
        )
        self.choice2_q1 = QuizChoice.objects.create(
            question=self.question1,
            text='London'
        )
        self.choice3_q1 = QuizChoice.objects.create(
            question=self.question1,
            text='Berlin'
        )

        self.question2 = QuizQuestion.objects.create(
            quiz=self.quiz,
            question_text='What is 2 + 2?',
            correct_answer='4',
            points=5
        )
        self.choice1_q2 = QuizChoice.objects.create(
            question=self.question2,
            text='3'
        )
        self.choice2_q2 = QuizChoice.objects.create(
            question=self.question2,
            text='4'
        )
        self.choice3_q2 = QuizChoice.objects.create(
            question=self.question2,
            text='5'
        )

        self.question3 = QuizQuestion.objects.create(
            quiz=self.quiz,
            question_text='Who wrote "Hamlet"?',
            correct_answer='Shakespeare',
            points=15
        )
        self.choice1_q3 = QuizChoice.objects.create(
            question=self.question3,
            text='Shakespeare'
        )
        self.choice2_q3 = QuizChoice.objects.create(
            question=self.question3,
            text='Dickens'
        )
        self.choice3_q3 = QuizChoice.objects.create(
            question=self.question3,
            text='Hemingway'
        )

        # mock user authorization
        self.client.credentials(HTTP_AUTHORIZATION='Username ' + self.user.username)

    def test_get_quiz_questions_success(self):
        url = reverse('get_quiz_questions', args=[self.quiz.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('quiz_name', response.data)
        self.assertIn('questions', response.data)
        self.assertEqual(len(response.data['questions']), 3)
        self.assertEqual(response.data['quiz_name'], self.quiz.name)

    def test_get_quiz_questions_invalid_quiz(self):
        url = reverse('get_quiz_questions', args=[999])  # assume 999 is invalid
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_check_quiz_eligibility_first_time(self):
        url = reverse('check_quiz_eligibility', args=[self.quiz.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['eligible'])
        self.assertTrue(response.data['can_earn_points'])

    def test_check_quiz_eligibility_within_cooldown(self):
        # create UserQuizScore，set completed at today
        UserQuizScore.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=20,
            correct_answers=2,
            completed_at=timezone.now()
        )

        url = reverse('check_quiz_eligibility', args=[self.quiz.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['eligible'])
        self.assertFalse(response.data['can_earn_points'])
        self.assertIn('remaining_time', response.data)
        self.assertIn('hours', response.data['remaining_time'])
        self.assertIn('minutes', response.data['remaining_time'])
        self.assertIn('seconds', response.data['remaining_time'])

    def test_check_quiz_eligibility_after_cooldown(self):
        # create UserQuizScore，set completed before 4 days
        UserQuizScore.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=20,
            correct_answers=2,
            completed_at=timezone.now() - timedelta(days=4)
        )

        url = reverse('check_quiz_eligibility', args=[self.quiz.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['eligible'])
        self.assertTrue(response.data['can_earn_points'])

    def test_check_quiz_eligibility_unauthorized(self):
        # no authorization
        self.client.credentials()

        url = reverse('check_quiz_eligibility', args=[self.quiz.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_submit_quiz_correct_answers(self):
        url = reverse('submit_quiz', args=[self.quiz.id])
        data = {
            'answers': {
                self.question1.id: 'Paris',
                self.question2.id: '4',
                self.question3.id: 'Shakespeare'
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Correct')
        self.assertEqual(response.data['total_score'], 30)  # 10 + 5 + 15

    def test_submit_quiz_incorrect_answers(self):
        url = reverse('submit_quiz', args=[self.quiz.id])
        data = {
            'answers': {
                self.question1.id: 'London',
                self.question2.id: '3',
                self.question3.id: 'Hemingway'
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Incorrect')
        self.assertEqual(response.data['total_score'], 0)

    def test_submit_quiz_partial_correct_answers(self):
        url = reverse('submit_quiz', args=[self.quiz.id])
        data = {
            'answers': {
                self.question1.id: 'Paris',
                self.question2.id: '3',
                self.question3.id: 'Hemingway'
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Correct')
        self.assertEqual(response.data['total_score'], 10)  # Only question1 correct

    def test_submit_quiz_invalid_quiz(self):
        url = reverse('submit_quiz', args=[999])  # assume 999 is invalid
        data = {
            'answers': {
                self.question1.id: 'Paris',
                self.question2.id: '4',
                self.question3.id: 'Shakespeare'
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_submit_quiz_missing_answers(self):
        url = reverse('submit_quiz', args=[self.quiz.id])
        data = {
            'answers': {
                self.question1.id: 'Paris',
                # lack question2 and question3
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # you may need to change here
        self.assertEqual(response.data['message'], 'Correct')
        self.assertEqual(response.data['total_score'], 10)  # Only question1 correct

    def test_submit_quiz_unauthorized(self):
        # no authorization
        self.client.credentials()

        url = reverse('submit_quiz', args=[self.quiz.id])
        data = {
            'answers': {
                self.question1.id: 'Paris',
                self.question2.id: '4',
                self.question3.id: 'Shakespeare'
            }
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_finalize_quiz_score_first_time(self):
        url = reverse('finalize_quiz_score', args=[self.quiz.id])
        data = {
            'username': self.user.username,
            'total_score': 25,
            'total_correct': 2
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Quiz completed. Your score has been recorded.')

        # if UserQuizScore created
        self.assertTrue(UserQuizScore.objects.filter(user=self.user, quiz=self.quiz).exists())

        # if user point updated
        points_log = PointsLog.objects.filter(user=self.user).aggregate(Sum('experience_points'))
        self.assertEqual(points_log['experience_points__sum'], 25)

    def test_finalize_quiz_score_within_cooldown(self):
        # create UserQuizScore，set completed at today
        UserQuizScore.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=20,
            correct_answers=2,
            completed_at=timezone.now()
        )

        # no need to create PointsLog，because views will use update_user_points
        # PointsLog.objects.create(
        #     user=self.user,
        #     experience_points=20,
        #     shop_points=0,
        #     timestamp=timezone.now()
        # )

        url = reverse('finalize_quiz_score', args=[self.quiz.id])
        data = {
            'username': self.user.username,
            'total_score': 15,
            'total_correct': 1
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Quiz completed. You did not earn points this time.')

        # if UserQuizScore create new record
        scores = UserQuizScore.objects.filter(user=self.user, quiz=self.quiz)
        self.assertEqual(scores.count(), 1)

        # if user points updated
        points_log = PointsLog.objects.filter(user=self.user).aggregate(Sum('experience_points'))
        self.assertEqual(points_log['experience_points__sum'], 20)

    def test_finalize_quiz_score_after_cooldown(self):
        # create UserQuizScore，set completed before 4 days
        UserQuizScore.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=20,
            correct_answers=2,
            completed_at=timezone.now() - timedelta(days=4)
        )

        url = reverse('finalize_quiz_score', args=[self.quiz.id])
        data = {
            'username': self.user.username,
            'total_score': 15,
            'total_correct': 1
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Quiz completed. Your score has been recorded.')

        # if UserQuizScore created
        self.assertEqual(UserQuizScore.objects.filter(user=self.user, quiz=self.quiz).count(), 2)

        # if user score updated
        points_log = PointsLog.objects.filter(user=self.user).aggregate(Sum('experience_points'))
        self.assertEqual(points_log['experience_points__sum'], 35)  # 20 + 15

    def test_finalize_quiz_score_missing_data(self):
        url = reverse('finalize_quiz_score', args=[self.quiz.id])
        data = {
            'username': self.user.username,
            # lack 'total_score' and 'total_correct'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_finalize_quiz_score_invalid_user(self):
        url = reverse('finalize_quiz_score', args=[self.quiz.id])
        data = {
            'username': 'nonexistentuser',
            'total_score': 15,
            'total_correct': 1
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_quiz_leaderboard_success(self):
        # create UserQuizScore
        UserQuizScore.objects.create(user=self.user, quiz=self.quiz, score=20, correct_answers=2, completed_at=timezone.now())
        UserQuizScore.objects.create(user=self.user2, quiz=self.quiz, score=15, correct_answers=1, completed_at=timezone.now())

        url = reverse('quiz_leaderboard', args=[self.quiz.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], self.user.username)
        self.assertEqual(response.data[0]['total_correct'], 2)
        self.assertEqual(response.data[1]['username'], self.user2.username)
        self.assertEqual(response.data[1]['total_correct'], 1)

    def test_quiz_leaderboard_no_scores(self):
        url = reverse('quiz_leaderboard', args=[self.quiz.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)

    def test_quiz_leaderboard_invalid_quiz(self):
        url = reverse('quiz_leaderboard', args=[999])  # assume 999 is invalid quiz_id
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
