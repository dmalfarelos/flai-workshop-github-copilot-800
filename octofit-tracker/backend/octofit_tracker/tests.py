from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserAPITestCase(APITestCase):
    """Test cases for User API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'name': 'Test Hero',
            'email': 'test.hero@test.com',
            'team': 'Test Team',
            'role': 'member',
            'avatar': 'test.png'
        }

    def test_create_user(self):
        """Test creating a new user"""
        response = self.client.post(reverse('user-list'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users(self):
        """Test listing all users"""
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamAPITestCase(APITestCase):
    """Test cases for Team API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            'name': 'Test Team',
            'description': 'A test team',
            'leader': 'Test Leader',
            'members': ['Test Leader', 'Member 1'],
            'total_points': 0
        }

    def test_create_team(self):
        """Test creating a new team"""
        response = self.client.post(reverse('team-list'), self.team_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_teams(self):
        """Test listing all teams"""
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITestCase(APITestCase):
    """Test cases for Activity API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'user_name': 'Test Hero',
            'user_email': 'test.hero@test.com',
            'team': 'Test Team',
            'activity_type': 'running',
            'duration_minutes': 30,
            'distance_km': 5.0,
            'calories_burned': 300,
            'points': 20,
            'date': datetime.now().isoformat(),
            'notes': 'Test run'
        }

    def test_create_activity(self):
        """Test logging a new activity"""
        response = self.client.post(reverse('activity-list'), self.activity_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_activities(self):
        """Test listing all activities"""
        response = self.client.get(reverse('activity-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITestCase(APITestCase):
    """Test cases for Leaderboard API endpoints"""

    def setUp(self):
        self.client = APIClient()

    def test_list_leaderboard(self):
        """Test listing leaderboard entries"""
        response = self.client.get(reverse('leaderboard-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_top_users(self):
        """Test getting top users from leaderboard"""
        response = self.client.get(reverse('leaderboard-top-users'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITestCase(APITestCase):
    """Test cases for Workout API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.workout_data = {
            'name': 'Test Workout',
            'description': 'A test workout routine',
            'category': 'strength_training',
            'difficulty': 'beginner',
            'duration_minutes': 30,
            'exercises': ['Push-ups', 'Squats'],
            'target_muscles': ['chest', 'legs'],
            'recommended_for': ['beginner']
        }

    def test_create_workout(self):
        """Test creating a new workout"""
        response = self.client.post(reverse('workout-list'), self.workout_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_workouts(self):
        """Test listing all workouts"""
        response = self.client.get(reverse('workout-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRootTestCase(APITestCase):
    """Test cases for API root endpoint"""

    def setUp(self):
        self.client = APIClient()

    def test_api_root(self):
        """Test API root returns correct structure"""
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('endpoints', response.data)
        self.assertIn('documentation', response.data)
