from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)  # Using the decorator to register the model
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture')  # Customize the fields you want to display in the admin list view
    search_fields = ('user__username', 'bio')  # Enable search by username or bio
