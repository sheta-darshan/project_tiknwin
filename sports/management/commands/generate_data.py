import random
from faker import Faker
from django.core.management.base import BaseCommand
from sports.models import SportCategory, Sport, SportDiscipline, Team, Player

fake = Faker()

class Command(BaseCommand):
    help = 'Generate 1000 fake sports data entries'

    def handle(self, *args, **kwargs):
        # Create SportCategories
        categories = ['Team Sports', 'Individual Sports', 'Racquet Sports', 'Water Sports', 'Winter Sports']
        category_objects = []
        for category in categories:
            category_obj, created = SportCategory.objects.get_or_create(name=category)
            category_objects.append(category_obj)

        # Create Sports
        sports = []
        for _ in range(200):
            sport_name = fake.word().capitalize()
            category = random.choice(category_objects)
            sport, created = Sport.objects.get_or_create(name=sport_name, category=category, is_olympic_sport=random.choice([True, False]), description=fake.sentence())
            sports.append(sport)

        # Create SportDisciplines
        disciplines = []
        for sport in sports:
            for _ in range(5):  # 5 disciplines per sport
                discipline_name = fake.word().capitalize()
                discipline, created = SportDiscipline.objects.get_or_create(sport=sport, name=discipline_name, description=fake.sentence())
                disciplines.append(discipline)

        # Create Teams
        teams = []
        for _ in range(500):  # 500 teams
            team_name = fake.word().capitalize() + " " + fake.word().capitalize()
            sport = random.choice(sports)
            team, created = Team.objects.get_or_create(name=team_name, sport=sport, logo=fake.image_url(), description=fake.sentence(), founded_year=fake.year(), history=fake.text(), city=fake.city(), stadium=fake.word().capitalize() + " Stadium")
            teams.append(team)

        # Create Players
        for _ in range(1000):  # 1000 players
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            sport = random.choice(sports)
            if sport is None:
                print("No sport available, skipping player creation.")
                continue  # Skip if no sport is available

            print(f"Creating player for sport: {sport.name}")  # Debug statement

            player = Player(
                first_name=first_name,
                last_name=last_name,
                profile_picture=fake.image_url(),
                sport=sport,
                bio=fake.text(),
                date_of_birth=fake.date_of_birth(),
                nationality=fake.country(),
                career_statistics=fake.text(),
                achievements=fake.text(),
                position=fake.word(),
                height=round(random.uniform(1.5, 2.0), 2),  # Height in meters
                weight=round(random.uniform(50, 100), 2),  # Weight in kg
            )
            
            # Check if the player instance is valid before saving
            try:
                player.save()
            except Exception as e:
                print(f"Error creating player {first_name} {last_name}: {e}")
                continue  # Skip this iteration if there was an error

            # Assign random teams and disciplines if available
            if teams:
                player.teams.set(random.sample(teams, random.randint(1, min(len(teams), 3))))  # Randomly assign 1 to 3 teams

            if disciplines:
                player.disciplines.set(random.sample(disciplines, random.randint(1, min(len(disciplines), 3))))  # Randomly assign 1 to 3 disciplines

            player.save()