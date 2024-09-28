from django.core.management.base import BaseCommand
from user.models import CustomUser, FriendList
import random

class Command(BaseCommand):
    help = 'empty friendlist for every user and assign 1 to 10 friends(this is onesided)'

    def handle(self, *args, **options):
        users = CustomUser.objects.all()  # get all user

        # empty friend list
        for user in users:
            friend_list, created = FriendList.objects.get_or_create(user=user)
            friend_list.friends.clear()
            self.stdout.write(self.style.WARNING(f'{user.username} friendlist has been empty'))

        # assign friend randomly
        for user in users:
            friend_list = FriendList.objects.get(user=user)
            
            # get user except self
            potential_friends = CustomUser.objects.exclude(id=user.id)
            
            # random choose num
            num_friends = random.randint(1, 10)
            
            # random choose friend
            friends = random.sample(list(potential_friends), num_friends)
            
            # Manually assign friends to current user without automatically updating reverse relationships
            for friend in friends:
                if not friend_list.friends.filter(id=friend.id).exists():
                    friend_list.friends.add(friend)
            
            self.stdout.write(self.style.SUCCESS(f'assign {user.username} with {num_friends} friends'))
