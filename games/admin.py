from django.contrib import admin
from .models import Event, TeamMatch, IndividualMatch, FlexibleMatch

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('sports',)
    ordering = ('start_date',)  # Optional: Order events by start date

@admin.register(TeamMatch)
class TeamMatchAdmin(admin.ModelAdmin):
    list_display = ('game', 'team1', 'team2', 'winner')
    search_fields = ('team1__name', 'team2__name', 'event__name')  # Updated to directly reference 'event'
    list_filter = ('game',)
    ordering = ('event__start_date',)  # Updated to order by event start date

@admin.register(IndividualMatch)
class IndividualMatchAdmin(admin.ModelAdmin):
    list_display = ('game', 'winner', 'runner_up1', 'runner_up2')
    search_fields = ('winner__first_name', 'runner_up1__first_name', 'runner_up2__first_name', 'event__name')  # Updated to directly reference 'event'
    list_filter = ('game',)
    ordering = ('event__start_date',)  # Updated to order by event start date

@admin.register(FlexibleMatch)
class FlexibleMatchAdmin(admin.ModelAdmin):
    list_display = ('game', 'is_team_based', 'winner', 'individual_winner')
    list_filter = ('is_team_based', 'game')
    search_fields = ('event__name',)  # Updated to directly reference 'event'
    ordering = ('event__start_date',)  # Updated to order by event start date
