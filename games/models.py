from django.db import models
from sports.models import Sport, Team, Player
from django.core.exceptions import ValidationError
from django.utils import timezone

class Event(models.Model):
    # Represents a sports event (e.g., T20 World Cup, US Open)
    name = models.CharField(max_length=100)  # Name of the event
    start_date = models.DateTimeField()  # Start date and time of the event
    end_date = models.DateTimeField()  # End date and time of the event
    description = models.TextField(blank=True, null=True)  # Optional description
    sports = models.ManyToManyField(Sport)  # Associated sports

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date.")
        super().clean()
    
class TeamMatch(models.Model):
    # Represents a team-based match within an event
    game = models.CharField(max_length=100)  # Name of the game
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)  # Associated sport
    date = models.DateTimeField()  # Date and time of the match
    status = models.CharField(max_length=50, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], default='scheduled')
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')  # Team 1
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')  # Team 2
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_team_matches')

    def __str__(self):
        return f"{self.event.name}: {self.team1} vs {self.team2}"

    def clean(self):
        if self.winner and self.winner not in [self.team1, self.team2]:
            raise ValidationError("Winner must be one of the participating teams.")
        super().clean()


class IndividualMatch(models.Model):
    # Represents an individual-based match within an event
    game = models.CharField(max_length=100)  # Name of the game
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)  # Associated sport
    date = models.DateTimeField()  # Date and time of the match
    status = models.CharField(max_length=50, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], default='scheduled')
    participants = models.ManyToManyField(Player)
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_individual_matches')
    runner_up1 = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='first_runner_up')
    runner_up2 = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='second_runner_up')

    def __str__(self):
        return f"{self.event.name}: Individual Match"

    def clean(self):
        if self.winner and self.winner not in self.participants.all():
            raise ValidationError("Winner must be one of the participants.")
        if self.runner_up1 and self.runner_up1 not in self.participants.all():
            raise ValidationError("1st Runner-up must be one of the participants.")
        if self.runner_up2 and self.runner_up2 not in self.participants.all():
            raise ValidationError("2nd Runner-up must be one of the participants.")
        super().clean()


class FlexibleMatch(models.Model):
    # Represents a flexible match that can involve teams or individuals
    game = models.CharField(max_length=100)  # Name of the game
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)  # Associated sport
    date = models.DateTimeField()  # Date and time of the match
    status = models.CharField(max_length=50, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], default='scheduled')
    is_team_based = models.BooleanField(default=True)
    participants = models.ManyToManyField(Team, blank=True)
    individual_participants = models.ManyToManyField(Player, blank=True)
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_flexible_matches')
    individual_winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_flexible_matches')

    def __str__(self):
        return f"{self.event.name}: Flexible Match"

    def clean(self):
        if self.is_team_based:
            if not self.participants.exists():
                raise ValidationError("Participants are required for a team-based match.")
            if self.winner and self.winner not in self.participants.all():
                raise ValidationError("Winner must be one of the participating teams.")
        else:
            if not self.individual_participants.exists():
                raise ValidationError("Individual participants are required for an individual-based match.")
            if self.individual_winner and self.individual_winner not in self.individual_participants.all():
                raise ValidationError("Individual winner must be one of the participants.")
        super().clean()
