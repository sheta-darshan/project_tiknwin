from django.db import models
from django.utils import timezone


class SportCategory(models.Model):
    # Represents categories of sports (e.g., Team Sports, Individual Sports)
    name = models.CharField(max_length=100, unique=True)  # Unique name for the category
    
    def __str__(self):
        return self.name


class Sport(models.Model):
    # Represents a specific sport (e.g., Football, Basketball)
    name = models.CharField(max_length=100)  # Name of the sport
    category = models.ForeignKey(SportCategory, on_delete=models.CASCADE)  # Foreign key to SportCategory
    is_olympic_sport = models.BooleanField(default=False)  # Indicates if the sport is Olympic
    description = models.TextField(blank=True, null=True)  # Optional description of the sport
    
    def __str__(self):
        return self.name


class SportDiscipline(models.Model):
    # Represents specific disciplines within a sport (e.g., 100m Sprint in Athletics)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)  # Foreign key to Sport
    name = models.CharField(max_length=100)  # Name of the discipline
    description = models.TextField(blank=True, null=True)  # Optional description of the discipline
    
    def __str__(self):
        return f"{self.name} - {self.sport.name}"  # Example: "100m Sprint - Athletics"


class Team(models.Model):
    # Represents a team participating in a sport (e.g., Mumbai Indians in Cricket)
    name = models.CharField(max_length=100)  # Name of the team
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)  # Foreign key to Sport
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)  # Team logo image
    description = models.TextField(blank=True, null=True)  # Optional description of the team
    founded_year = models.IntegerField(blank=True, null=True)  # Year the team was founded
    history = models.TextField(blank=True, null=True)  # Detailed history of the team
    city = models.CharField(max_length=100, blank=True, null=True)  # City where the team is based
    stadium = models.CharField(max_length=100, blank=True, null=True)  # Name of the team's home stadium
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the team was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the team was last updated

    class Meta:
        unique_together = ('name', 'sport')  # Unique constraint for team name per sport

    def __str__(self):
        return self.name  # Example: "Mumbai Indians"


class Player(models.Model):
    # Represents an individual player (e.g., Virat Kohli in Cricket)
    first_name = models.CharField(max_length=100)  # First name of the player
    last_name = models.CharField(max_length=100)  # Last name of the player
    profile_picture = models.ImageField(upload_to='player_profiles/', blank=True, null=True)  # Player profile picture
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Biography of the player
    date_of_birth = models.DateField(null=True, blank=True)  # Player's date of birth
    nationality = models.CharField(max_length=100, blank=True, null=True)  # Player's nationality
    career_statistics = models.TextField(blank=True, null=True)  # Player's career statistics (JSON or plain text)
    achievements = models.TextField(blank=True, null=True)  # Notable achievements and awards
    position = models.CharField(max_length=100, blank=True, null=True)  # Position played
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Height in meters
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Weight in kilograms
    teams = models.ManyToManyField(Team, blank=True)  # Player can belong to multiple teams
    disciplines = models.ManyToManyField(SportDiscipline, blank=True)  # Player can participate in multiple disciplines
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the player was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the player was last updated

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Example: "Virat Kohli"


# Optional: Custom manager for additional queries (example)
class PlayerManager(models.Manager):
    def with_teams(self):
        return self.filter(teams__isnull=False)  # Custom method to get players associated with teams


# Usage of the custom manager in Player model
Player.objects = PlayerManager()
