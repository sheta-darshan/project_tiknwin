from django.contrib import admin
from .models import SportCategory, Sport, SportDiscipline, Team, Player

class SportCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_olympic_sport')
    list_filter = ('category', 'is_olympic_sport')
    search_fields = ('name',)
    ordering = ('name',)

class SportDisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport')
    list_filter = ('sport',)
    search_fields = ('name',)
    ordering = ('sport', 'name')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'city', 'founded_year', 'created_at')
    list_filter = ('sport', 'city')
    search_fields = ('name',)
    ordering = ('name',)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'nationality', 'position', 'height', 'weight')
    list_filter = ('sport', 'teams', 'nationality', 'position')  # Changed 'team' to 'teams'
    search_fields = ('first_name', 'last_name', 'nationality')
    ordering = ('last_name', 'first_name')

# Register your models here
admin.site.register(SportCategory, SportCategoryAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(SportDiscipline, SportDisciplineAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
