from django.core.management.base import BaseCommand
from user.models import CustomUser
import random

class Command(BaseCommand):
    help = 'Generates test users for the application'

    def handle(self, *args, **kwargs):
        locations = ['Melbourne', 'Sydney']
        for i in range(20, 120):  # id from 20 to 100
            accumulated_points = random.randint(10, 1000)
            spendable_points = random.randint(0, accumulated_points)  # make sure spendable will not greater than accumulated

            user = CustomUser.objects.create_user(
                username=f'testUser{i}',
                email=f'testUser{i}@example.com',
                title=f'User Title {i}',  # user title cannot be empty
                is_superuser=False,  # not super user
                location=random.choice(locations),
                points_accumulated=accumulated_points,
                points_spendable=spendable_points
            )
            user.save()
            print(f'Created {user.username}')
