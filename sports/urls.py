from django.urls import path
from .views import (
    SportCategoryListView,
    SportListView,
    SportDetailView,
    TeamDetailView,
    PlayerDetailView,
    SportDisciplineListView,
    SportDisciplineDetailView,
)

app_name = 'sports'

urlpatterns = [
    path('categories/', SportCategoryListView.as_view(), name='sport_category_list'),
    path('sports/<int:category_id>/', SportListView.as_view(), name='sport_list'),
    path('sports/<int:category_id>/<int:pk>/', SportDetailView.as_view(), name='sport_detail'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('players/<int:pk>/', PlayerDetailView.as_view(), name='player_detail'),
    path('disciplines/', SportDisciplineListView.as_view(), name='sport_discipline_list'),
    path('disciplines/<int:pk>/', SportDisciplineDetailView.as_view(), name='sport_discipline_detail'),
]
