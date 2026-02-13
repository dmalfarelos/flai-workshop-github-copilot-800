from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write(self.style.SUCCESS('Connected to MongoDB'))

        # Delete existing data
        self.stdout.write('Deleting existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email field
        db.users.create_index([("email", 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))

        # Marvel Team Users
        marvel_users = [
            {
                "name": "Tony Stark",
                "email": "tony.stark@marvel.com",
                "team": "Team Marvel",
                "role": "team_lead",
                "avatar": "ironman.png",
                "created_at": datetime.now() - timedelta(days=30)
            },
            {
                "name": "Steve Rogers",
                "email": "steve.rogers@marvel.com",
                "team": "Team Marvel",
                "role": "member",
                "avatar": "captainamerica.png",
                "created_at": datetime.now() - timedelta(days=28)
            },
            {
                "name": "Natasha Romanoff",
                "email": "natasha.romanoff@marvel.com",
                "team": "Team Marvel",
                "role": "member",
                "avatar": "blackwidow.png",
                "created_at": datetime.now() - timedelta(days=27)
            },
            {
                "name": "Bruce Banner",
                "email": "bruce.banner@marvel.com",
                "team": "Team Marvel",
                "role": "member",
                "avatar": "hulk.png",
                "created_at": datetime.now() - timedelta(days=26)
            },
            {
                "name": "Thor Odinson",
                "email": "thor.odinson@marvel.com",
                "team": "Team Marvel",
                "role": "member",
                "avatar": "thor.png",
                "created_at": datetime.now() - timedelta(days=25)
            }
        ]

        # DC Team Users
        dc_users = [
            {
                "name": "Bruce Wayne",
                "email": "bruce.wayne@dc.com",
                "team": "Team DC",
                "role": "team_lead",
                "avatar": "batman.png",
                "created_at": datetime.now() - timedelta(days=30)
            },
            {
                "name": "Clark Kent",
                "email": "clark.kent@dc.com",
                "team": "Team DC",
                "role": "member",
                "avatar": "superman.png",
                "created_at": datetime.now() - timedelta(days=29)
            },
            {
                "name": "Diana Prince",
                "email": "diana.prince@dc.com",
                "team": "Team DC",
                "role": "member",
                "avatar": "wonderwoman.png",
                "created_at": datetime.now() - timedelta(days=28)
            },
            {
                "name": "Barry Allen",
                "email": "barry.allen@dc.com",
                "team": "Team DC",
                "role": "member",
                "avatar": "flash.png",
                "created_at": datetime.now() - timedelta(days=27)
            },
            {
                "name": "Arthur Curry",
                "email": "arthur.curry@dc.com",
                "team": "Team DC",
                "role": "member",
                "avatar": "aquaman.png",
                "created_at": datetime.now() - timedelta(days=26)
            }
        ]

        # Insert users
        all_users = marvel_users + dc_users
        result = db.users.insert_many(all_users)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(result.inserted_ids)} users'))

        # Create Teams
        teams = [
            {
                "name": "Team Marvel",
                "description": "Earth's Mightiest Heroes",
                "leader": "Tony Stark",
                "members": ["Tony Stark", "Steve Rogers", "Natasha Romanoff", "Bruce Banner", "Thor Odinson"],
                "total_points": 0,
                "created_at": datetime.now() - timedelta(days=30)
            },
            {
                "name": "Team DC",
                "description": "Justice League United",
                "leader": "Bruce Wayne",
                "members": ["Bruce Wayne", "Clark Kent", "Diana Prince", "Barry Allen", "Arthur Curry"],
                "total_points": 0,
                "created_at": datetime.now() - timedelta(days=30)
            }
        ]

        result = db.teams.insert_many(teams)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(result.inserted_ids)} teams'))

        # Create Activities
        activity_types = ["running", "cycling", "swimming", "strength_training", "yoga", "hiking"]
        activities = []

        for user in all_users:
            # Generate 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity = {
                    "user_name": user["name"],
                    "user_email": user["email"],
                    "team": user["team"],
                    "activity_type": random.choice(activity_types),
                    "duration_minutes": random.randint(20, 120),
                    "distance_km": round(random.uniform(2.0, 15.0), 2),
                    "calories_burned": random.randint(150, 800),
                    "points": random.randint(10, 50),
                    "date": datetime.now() - timedelta(days=random.randint(1, 30)),
                    "notes": f"Training session {i+1}"
                }
                activities.append(activity)

        result = db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(result.inserted_ids)} activities'))

        # Calculate points for leaderboard
        from collections import defaultdict
        user_points = defaultdict(int)
        team_points = defaultdict(int)

        for activity in activities:
            user_points[activity["user_email"]] += activity["points"]
            team_points[activity["team"]] += activity["points"]

        # Create Leaderboard entries
        leaderboard = []
        for user in all_users:
            leaderboard.append({
                "user_name": user["name"],
                "user_email": user["email"],
                "team": user["team"],
                "total_points": user_points[user["email"]],
                "rank": 0,  # Will be calculated
                "last_updated": datetime.now()
            })

        # Sort by points and assign ranks
        leaderboard.sort(key=lambda x: x["total_points"], reverse=True)
        for idx, entry in enumerate(leaderboard):
            entry["rank"] = idx + 1

        result = db.leaderboard.insert_many(leaderboard)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(result.inserted_ids)} leaderboard entries'))

        # Update team points
        db.teams.update_one({"name": "Team Marvel"}, {"$set": {"total_points": team_points["Team Marvel"]}})
        db.teams.update_one({"name": "Team DC"}, {"$set": {"total_points": team_points["Team DC"]}})

        # Create Workout suggestions
        workouts = [
            {
                "name": "Hero's Strength Training",
                "description": "Build superhero strength with compound exercises",
                "category": "strength_training",
                "difficulty": "intermediate",
                "duration_minutes": 45,
                "exercises": [
                    "Bench Press - 3 sets of 10 reps",
                    "Squats - 3 sets of 12 reps",
                    "Deadlifts - 3 sets of 8 reps",
                    "Pull-ups - 3 sets of max reps"
                ],
                "target_muscles": ["chest", "legs", "back", "core"],
                "recommended_for": ["beginner", "intermediate"]
            },
            {
                "name": "Flash Speed Run",
                "description": "Interval training for speed and endurance",
                "category": "running",
                "difficulty": "advanced",
                "duration_minutes": 30,
                "exercises": [
                    "5 min warm-up jog",
                    "8x 400m sprints with 90s recovery",
                    "5 min cool-down jog"
                ],
                "target_muscles": ["legs", "cardiovascular"],
                "recommended_for": ["intermediate", "advanced"]
            },
            {
                "name": "Warrior Yoga Flow",
                "description": "Flexibility and mindfulness training",
                "category": "yoga",
                "difficulty": "beginner",
                "duration_minutes": 30,
                "exercises": [
                    "Sun Salutation A - 5 rounds",
                    "Warrior Poses I, II, III",
                    "Tree Pose",
                    "Savasana - 5 minutes"
                ],
                "target_muscles": ["full_body", "flexibility"],
                "recommended_for": ["all_levels"]
            },
            {
                "name": "Aquatic Endurance",
                "description": "Swimming workout for full-body conditioning",
                "category": "swimming",
                "difficulty": "intermediate",
                "duration_minutes": 60,
                "exercises": [
                    "400m freestyle warm-up",
                    "8x 100m intervals (various strokes)",
                    "200m cool-down"
                ],
                "target_muscles": ["full_body", "cardiovascular"],
                "recommended_for": ["intermediate", "advanced"]
            },
            {
                "name": "Mountain Conquest",
                "description": "Hiking workout with elevation gains",
                "category": "hiking",
                "difficulty": "advanced",
                "duration_minutes": 120,
                "exercises": [
                    "Steady uphill climb",
                    "Peak summit",
                    "Controlled descent"
                ],
                "target_muscles": ["legs", "cardiovascular", "endurance"],
                "recommended_for": ["advanced"]
            }
        ]

        result = db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS(f'Inserted {len(result.inserted_ids)} workout suggestions'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Users: {db.users.count_documents({})}')
        self.stdout.write(f'Teams: {db.teams.count_documents({})}')
        self.stdout.write(f'Activities: {db.activities.count_documents({})}')
        self.stdout.write(f'Leaderboard: {db.leaderboard.count_documents({})}')
        self.stdout.write(f'Workouts: {db.workouts.count_documents({})}')
        self.stdout.write(self.style.SUCCESS('\nTeam Marvel Points: ' + str(team_points["Team Marvel"])))
        self.stdout.write(self.style.SUCCESS('Team DC Points: ' + str(team_points["Team DC"])))

        client.close()
