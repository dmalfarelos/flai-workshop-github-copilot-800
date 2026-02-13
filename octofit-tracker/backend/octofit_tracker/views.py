from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    Provides endpoints for listing, creating, retrieving, updating, and deleting users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['team', 'role']
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get all users grouped by team"""
        team = request.query_params.get('team', None)
        if team:
            users = User.objects.filter(team=team)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response({'error': 'Team parameter is required'}, status=400)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teams.
    Provides endpoints for listing, creating, retrieving, updating, and deleting teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'total_points', 'created_at']
    ordering = ['-total_points']

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        users = User.objects.filter(team=team.name)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing activities.
    Provides endpoints for logging and tracking fitness activities.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user_email', 'team', 'activity_type']
    search_fields = ['user_name', 'activity_type']
    ordering_fields = ['date', 'points', 'calories_burned']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get all activities for a specific user"""
        user_email = request.query_params.get('email', None)
        if user_email:
            activities = Activity.objects.filter(user_email=user_email)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'Email parameter is required'}, status=400)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get all activities for a specific team"""
        team = request.query_params.get('team', None)
        if team:
            activities = Activity.objects.filter(team=team)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({'error': 'Team parameter is required'}, status=400)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing the leaderboard.
    Provides endpoints for viewing competitive rankings.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['team']
    ordering_fields = ['rank', 'total_points']
    ordering = ['rank']

    @action(detail=False, methods=['get'])
    def top_users(self, request):
        """Get top N users from the leaderboard"""
        limit = int(request.query_params.get('limit', 10))
        top_users = Leaderboard.objects.all()[:limit]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard for a specific team"""
        team = request.query_params.get('team', None)
        if team:
            leaderboard = Leaderboard.objects.filter(team=team)
            serializer = self.get_serializer(leaderboard, many=True)
            return Response(serializer.data)
        return Response({'error': 'Team parameter is required'}, status=400)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workout suggestions.
    Provides endpoints for personalized workout recommendations.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'duration_minutes']
    ordering = ['name']

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts by difficulty level"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Difficulty parameter is required'}, status=400)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get workouts by category"""
        category = request.query_params.get('category', None)
        if category:
            workouts = Workout.objects.filter(category=category)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({'error': 'Category parameter is required'}, status=400)
