from django.urls import path
from . import views


app_name = 'games'

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('team-match/<int:pk>/', views.TeamMatchDetailView.as_view(), name='team-match-detail'),
    path('individual-match/<int:pk>/', views.IndividualMatchDetailView.as_view(), name='individual-match-detail'),
    path('flexible-match/<int:pk>/', views.FlexibleMatchDetailView.as_view(), name='flexible-match-detail'),
    path('sports/<int:pk>/', views.SportDetailView.as_view(), name='sport-detail'),
    path('team-match/<int:pk>/', views.TeamMatchDetailView.as_view(), name='team-match-detail'),
    path('individual-match/<int:pk>/', views.IndividualMatchDetailView.as_view(), name='individual-match-detail'),
    path('flexible-match/<int:pk>/', views.FlexibleMatchDetailView.as_view(), name='flexible-match-detail'),

]
