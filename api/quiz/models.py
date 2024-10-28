from django.db import models
from user.models import CustomUser
from django.db import transaction
from django.utils import timezone


# Quiz Model - Stores information about the quiz itself
class Quiz(models.Model):
    name = models.CharField(max_length=255)  # Quiz name
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the quiz was created

    def __str__(self):
        return self.name


# QuizQuestion Model - Stores questions associated with a specific quiz
class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')  # Each question belongs to a quiz
    question_text = models.CharField(max_length=255)  # The question itself
    correct_answer = models.CharField(max_length=255)  # Correct answer for the question
    points = models.IntegerField(default=0)  # Points awarded for answering this question correctly

    def __str__(self):
        return self.question_text


# QuizChoice Model - Stores multiple choices for a question
class QuizChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='choices')  # Belongs to a specific question
    text = models.CharField(max_length=255)  # The text for each choice/option

    def __str__(self):
        return self.text


# UserQuizScore Model - Stores the scores of users who take a quiz
class UserQuizScore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # The user who took the quiz
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # The quiz taken by the user
    score = models.IntegerField(default=0)  # The score the user achieved on the quiz
    completed_at = models.DateTimeField(default=timezone.now)  # When the quiz was completed
    correct_answers = models.IntegerField(default=0) # number of correct answer

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name} - {self.score}"


# Function to update user points based on quiz completion
@transaction.atomic
def update_user_points_after_quiz(user, quiz_score):
    # Ensure that the function runs in a transaction
    user.experience_points += quiz_score  # Add the score to user's experience points
    user.save()  # Save the updated user data

    # You can also log this score update in PointsLog if necessary
    # PointsLog.objects.create(
    #     user=user,
    #     experience_points=user.experience_points,
    #     shop_points=user.shop_points  # Assuming you want to track shop points as well
    # )
