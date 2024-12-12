from django.core.management.base import BaseCommand
from sports.models import SportCategory, Sport, SportDiscipline, Team, Player

class Command(BaseCommand):
    help = 'Delete all sports data entries'

    def handle(self, *args, **kwargs):
        Player.objects.all().delete()  # Delete all players
        Team.objects.all().delete()     # Delete all teams
        SportDiscipline.objects.all().delete()  # Delete all disciplines
        Sport.objects.all().delete()     # Delete all sports
        SportCategory.objects.all().delete()  # Delete all categories

        self.stdout.write(self.style.SUCCESS('Successfully deleted all sports data entries.'))