from django.urls import path
from .views import UserProfileUpdateView, UserProfileView


urlpatterns = [
    path('', UserProfileView.as_view(), name='profile'),
    path('edit/', UserProfileUpdateView.as_view(), name='edit_profile'),
]
