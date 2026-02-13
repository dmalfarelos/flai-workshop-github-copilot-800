from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'team', 'role', 'created_at']
    list_filter = ['team', 'role', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['name']
    readonly_fields = ['created_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'total_points', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'leader']
    ordering = ['-total_points']
    readonly_fields = ['created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'activity_type', 'team', 'duration_minutes', 
                    'distance_km', 'points', 'date']
    list_filter = ['activity_type', 'team', 'date']
    search_fields = ['user_name', 'user_email', 'activity_type']
    ordering = ['-date']
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['rank', 'user_name', 'team', 'total_points', 'last_updated']
    list_filter = ['team']
    search_fields = ['user_name', 'user_email']
    ordering = ['rank']
    readonly_fields = ['last_updated']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'difficulty', 'duration_minutes']
    list_filter = ['category', 'difficulty']
    search_fields = ['name', 'description']
    ordering = ['name']
