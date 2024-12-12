from django.views.generic import ListView, DetailView
from .models import SportCategory, Sport, SportDiscipline, Team, Player
from django.contrib.auth.mixins import LoginRequiredMixin


class SportCategoryListView(LoginRequiredMixin, ListView):
    model = SportCategory
    template_name = 'sports/sport_category_list.html'
    context_object_name = 'categories'

class SportListView(ListView):
    model = Sport
    template_name = 'sports/sport_list.html'
    context_object_name = 'sports'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Sport.objects.filter(category_id=category_id)
        return Sport.objects.none()

class SportDetailView(LoginRequiredMixin, DetailView):
    model = Sport
    template_name = 'sports/sport_detail.html'
    context_object_name = 'sport'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplines'] = self.object.sportdiscipline_set.all()
        context['teams'] = self.object.team_set.all()
        return context

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'sports/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.object.player_set.all()
        context['sport'] = self.object.sport  # Add sport context for navigation
        return context

class PlayerDetailView(LoginRequiredMixin, DetailView):
    model = Player
    template_name = 'sports/player_detail.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = self.object.teams.all()  # Show teams for the player
        return context

class SportDisciplineListView(LoginRequiredMixin, ListView):
    model = SportDiscipline
    template_name = 'sports/sport_discipline_list.html'
    context_object_name = 'disciplines'

    def get_queryset(self):
        sport_id = self.kwargs.get('sport_id')
        if sport_id:
            return SportDiscipline.objects.filter(sport_id=sport_id)
        return SportDiscipline.objects.none()

class SportDisciplineDetailView(LoginRequiredMixin, DetailView):
    model = SportDiscipline
    template_name = 'sports/sport_discipline_detail.html'
    context_object_name = 'discipline'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sport'] = self.object.sport  # Provide sport context
        return context
