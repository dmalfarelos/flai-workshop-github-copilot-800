from djongo import models
from bson import ObjectId


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    team = models.CharField(max_length=200)
    role = models.CharField(max_length=50)
    avatar = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        managed = False

    def __str__(self):
        return self.name


class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    leader = models.CharField(max_length=200)
    members = models.JSONField(default=list)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teams'
        managed = False

    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    team = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    distance_km = models.FloatField()
    calories_burned = models.IntegerField()
    points = models.IntegerField()
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'
        managed = False

    def __str__(self):
        return f"{self.user_name} - {self.activity_type}"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    team = models.CharField(max_length=200)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        managed = False
        ordering = ['rank']

    def __str__(self):
        return f"{self.rank}. {self.user_name} - {self.total_points} points"


class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    duration_minutes = models.IntegerField()
    exercises = models.JSONField(default=list)
    target_muscles = models.JSONField(default=list)
    recommended_for = models.JSONField(default=list)

    class Meta:
        db_table = 'workouts'
        managed = False

    def __str__(self):
        return self.name
