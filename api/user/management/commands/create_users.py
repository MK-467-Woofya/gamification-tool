from django.core.management.base import BaseCommand
from user.models import CustomUser
import random

class Command(BaseCommand):
    help = 'Generates test users for the application'

    def handle(self, *args, **kwargs):
        locations = ['Melbourne', 'Sydney']
        for i in range(20, 120):  # id from 20 to 100
            user_exp_points = random.randint(10, 1000)
            user_shop_points = random.randint(0, user_exp_points)  # make sure spendable will not greater than total experience

            user = CustomUser.objects.create_user(
                username=f'testUser{i}',
                location=random.choice(locations),
                experience_points=user_exp_points,
                shop_points=user_shop_points,
                is_admin=False
            )
            user.save()
            print(f'Created {user.username}')
