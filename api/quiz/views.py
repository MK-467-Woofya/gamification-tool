from user.models import update_user_points  # to update user score
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from user.models import CustomUser
from .models import Quiz, QuizQuestion, UserQuizScore

import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_quiz_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    question_list = [
        {
            'id': q.id,
            'question_text': q.question_text,
            'choices': [{'id': c.id, 'text': c.text} for c in q.choices.all()],
            'points': q.points,
        } for q in questions
    ]
    return Response({'quiz_name': quiz.name, 'questions': question_list})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def submit_quiz(request, quiz_id):
    # get user name
    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Username '):
        return Response({'error': 'Unauthorized: Username is required'}, status=401)

    username = authorization_header.split(' ')[1]
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=404)

    # get quiz
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers = request.data.get('answers', {})
    
    total_score = 0
    for question_id, user_answer in answers.items():
        question = get_object_or_404(QuizQuestion, id=question_id)
        
        # correct answer
        if question.correct_answer.strip().lower() == user_answer.strip().lower():
            total_score += question.points

    # record score
    UserQuizScore.objects.create(user=user, quiz=quiz, score=total_score)

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

    update_user_points(user, total_score, 0)

    return Response({'message': 'User score updated successfully'})


