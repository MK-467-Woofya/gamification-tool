from django.core.management.base import BaseCommand
from user.models import CustomUser, PointsLog

class Command(BaseCommand):
    help = 'Creates missing PointsLog entries for users without one'

    def handle(self, *args, **options):
        users_without_logs = CustomUser.objects.exclude(
            id__in=PointsLog.objects.values_list('user_id', flat=True)
        )
        for user in users_without_logs:
            PointsLog.objects.create(
                user=user,
                points_accumulated=user.points_accumulated,
                points_spendable=user.points_spendable
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created PointsLog entries for {users_without_logs.count()} users.'))
