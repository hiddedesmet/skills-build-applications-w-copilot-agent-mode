from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
import json
from pathlib import Path

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Load test data from JSON file
        test_data_path = Path(settings.BASE_DIR) / 'octofit_tracker' / 'test_data.json'
        with open(test_data_path, 'r') as file:
            data = json.load(file)

        # Populate users
        for user_data in data['users']:
            User.objects.update_or_create(username=user_data['username'], defaults=user_data)

        # Populate teams
        for team_data in data['teams']:
            members = [User.objects.get(username=member) for member in team_data.pop('members')]
            team, created = Team.objects.update_or_create(name=team_data['name'], defaults=team_data)
            team.members.set(members)

        # Populate activities
        for activity_data in data['activities']:
            user = User.objects.get(username=activity_data.pop('user'))
            Activity.objects.update_or_create(user=user, activity_type=activity_data['activity_type'], defaults=activity_data)

        # Populate leaderboard
        for leaderboard_data in data['leaderboard']:
            user = User.objects.get(username=leaderboard_data.pop('user'))
            Leaderboard.objects.update_or_create(user=user, defaults=leaderboard_data)

        # Populate workouts
        for workout_data in data['workouts']:
            Workout.objects.update_or_create(name=workout_data['name'], defaults=workout_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))