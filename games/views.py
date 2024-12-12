from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Sport, Event, TeamMatch, IndividualMatch, FlexibleMatch

class EventListView(ListView):
    model = Event
    template_name = 'games/event_list.html'  # Specify your template
    context_object_name = 'events'  # Name used in the template to reference the list

    def get_queryset(self):
        return Event.objects.all().order_by('-start_date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'games/event_detail.html'  # Specify your template
    context_object_name = 'event'  # Name used in the template to reference the object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['team_matches'] = TeamMatch.objects.filter(event=event)
        context['individual_matches'] = IndividualMatch.objects.filter(event=event)
        context['flexible_matches'] = FlexibleMatch.objects.filter(event=event)
        return context

class SportDetailView(DetailView):
    model = Sport
    template_name = 'games/sport_detail.html'  # or 'sports/sport_detail.html' depending on the structure
    context_object_name = 'sport'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sport = self.get_object()

        # Add related matches to the context
        context['team_matches'] = TeamMatch.objects.filter(sport=sport)
        context['individual_matches'] = IndividualMatch.objects.filter(sport=sport)
        context['flexible_matches'] = FlexibleMatch.objects.filter(sport=sport)

        return context
    
class TeamMatchDetailView(DetailView):
    model = TeamMatch
    template_name = 'games/team_match_detail.html'

class IndividualMatchDetailView(DetailView):
    model = IndividualMatch
    template_name = 'games/individual_match_detail.html'

class FlexibleMatchDetailView(DetailView):
    model = FlexibleMatch
    template_name = 'games/flexible_match_detail.html'
