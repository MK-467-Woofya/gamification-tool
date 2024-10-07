from user.models import update_user_points  # to update user score
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from user.models import CustomUser
from .models import Quiz, QuizQuestion, UserQuizScore

import logging
import random  # Import random module to enable random selection
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_quiz_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # Randomly select 3 questions from the quiz
    all_questions = list(quiz.questions.all())
    selected_questions = random.sample(all_questions, k=3)  # randomly choose 3 quiz(can change k value here)
    question_list = [
        {
            'id': q.id,
            'question_text': q.question_text,
            'choices': [{'id': c.id, 'text': c.text} for c in q.choices.all()],
            'points': q.points,
        } for q in selected_questions
    ]
    return Response({'quiz_name': quiz.name, 'questions': question_list})

from datetime import datetime, timedelta, timezone

@api_view(['GET'])
@permission_classes([AllowAny])
def check_quiz_eligibility(request, quiz_id):
    # Get username from request
    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Username '):
        return Response({'error': 'Unauthorized: Username is required'}, status=401)

    username = authorization_header.split(' ')[1]
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)

    # Get the last time the user completed the quiz
    last_score = UserQuizScore.objects.filter(user=user, quiz_id=quiz_id).order_by('-completed_at').first()

    if last_score:
        time_since_last_completion = datetime.now(timezone.utc) - last_score.completed_at
        if time_since_last_completion < timedelta(days=3):
            # Calculate remaining time
            remaining_time = timedelta(days=3) - time_since_last_completion
            remaining_seconds = int(remaining_time.total_seconds())
            hours, remainder = divmod(remaining_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            return Response({
                'eligible': True,
                'can_earn_points': False,
                'message': 'You need to wait before earning points again.',
                'remaining_time': {
                    'hours': hours,
                    'minutes': minutes,
                    'seconds': seconds
                }
            })
        else:
            return Response({'eligible': True, 'can_earn_points': True})
    else:
        # User hasn't taken the quiz before
        return Response({'eligible': True, 'can_earn_points': True})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def submit_quiz(request, quiz_id):
    # Get user name
    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Username '):
        return Response({'error': 'Unauthorized: Username is required'}, status=401)

    username = authorization_header.split(' ')[1]
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)

    # Get quiz
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers = request.data.get('answers', {})

    total_score = 0
    for question_id, user_answer in answers.items():
        question = get_object_or_404(QuizQuestion, id=question_id)

        # Correct answer
        if question.correct_answer.strip().lower() == user_answer.strip().lower():
            total_score += question.points

    # Do not create UserQuizScore here

    return Response({'message': 'Correct' if total_score > 0 else 'Incorrect', 'total_score': total_score})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def finalize_quiz_score(request, quiz_id):
    logger.debug(f"Request data: {request.data}")

    username = request.data.get('username')
    total_score = request.data.get('total_score')

    if not username or total_score is None:
        return Response({'error': 'Username and total score are required'}, status=400)

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)

    # Check if 3 days have passed since last completion
    last_score = UserQuizScore.objects.filter(user=user, quiz_id=quiz_id).order_by('-completed_at').first()

    if last_score:
        time_since_last_completion = datetime.now(timezone.utc) - last_score.completed_at
        if time_since_last_completion < timedelta(days=3):
            # Do not award points or update last completion time
            message = "Quiz completed. You did not earn points this time."
            return Response({'message': message})
        else:
            # Award points and update last completion time
            update_user_points(user, total_score, 0)
            # Record the quiz completion
            UserQuizScore.objects.create(user=user, quiz_id=quiz_id, score=total_score)
            return Response({'message': 'Quiz completed. Your score has been recorded.'})
    else:
        # First time taking the quiz, award points
        update_user_points(user, total_score, 0)
        # Record the quiz completion
        UserQuizScore.objects.create(user=user, quiz_id=quiz_id, score=total_score)
        return Response({'message': 'Quiz completed. Your score has been recorded.'})

