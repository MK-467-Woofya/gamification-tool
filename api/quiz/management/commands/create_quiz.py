from django.core.management.base import BaseCommand
from quiz.models import Quiz, QuizQuestion

class Command(BaseCommand):
    help = 'Create sample quiz and questions about dogs'

    def handle(self, *args, **kwargs):
        # create a new quiz
        quiz, created = Quiz.objects.get_or_create(name="Dog Knowledge Quiz")

        # sample questions with choices
        questions = [
            {
                'question_text': 'What is the most popular breed of dog in the world?',
                'correct_answer': 'Labrador Retriever',
                'choices': ['Labrador Retriever', 'German Shepherd', 'Poodle', 'Bulldog'],
                'points': 10,
            },
            {
                'question_text': 'What is the average lifespan of a domestic dog?',
                'correct_answer': '10-13 years',
                'choices': ['7-9 years', '10-13 years', '14-16 years', '17-20 years'],
                'points': 10,
            },
            {
                'question_text': 'Which dog breed is known for its blue-black tongue?',
                'correct_answer': 'Chow Chow',
                'choices': ['Chow Chow', 'Shih Tzu', 'Labrador Retriever', 'Dalmatian'],
                'points': 10,
            },
            {
                'question_text': 'What is the fastest dog breed?',
                'correct_answer': 'Greyhound',
                'choices': ['Greyhound', 'Bulldog', 'Poodle', 'Beagle'],
                'points': 10,
            },
            {
                'question_text': 'Which dog breed is commonly used by police forces?',
                'correct_answer': 'German Shepherd',
                'choices': ['German Shepherd', 'Golden Retriever', 'Shih Tzu', 'Dachshund'],
                'points': 10,
            }
        ]

        # create questions with choices
        for question_data in questions:
            question = QuizQuestion.objects.create(
                quiz=quiz,
                question_text=question_data['question_text'],
                correct_answer=question_data['correct_answer'],
                points=question_data['points']
            )
            # assuming choices is a ManyToManyField related to QuizQuestion or CharField to store in JSON
            for choice in question_data['choices']:
                question.choices.create(text=choice)

        self.stdout.write(self.style.SUCCESS('Successfully created quiz and questions with choices!'))
