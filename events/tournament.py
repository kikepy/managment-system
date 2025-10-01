from .event import Event
from .validation import validate_tournament
import math
from datetime import timedelta

class Tournament(Event):
    def __init__(self, name, date, location, sport, teams, format, specific_days=None, schedule_format="consecutive"):
        validate_tournament(teams=teams, format=format, date=date)
        super().__init__(name, date, location, sport, event_type="tournament")
        self.date = date  # Ensure the date is set
        self.teams = teams
        self.format = format
        self.specific_days = specific_days
        self.schedule_format = schedule_format
        self.schedule = self.create_schedule(sport, len(teams), format, specific_days, schedule_format)

    def calculate_duration(self, sport, num_teams, format):
        match_duration = self.calculate_total_duration(sport)
        print(f"Match duration: {match_duration}")  # Debugging

        if format == "knockout":
            total_matches = num_teams - 1
        elif format == "round-robin":
            total_matches = num_teams * (num_teams - 1) // 2
        elif format == "mixed":
            total_matches = (num_teams - 1) + (num_teams * (num_teams - 1) // 2)
        else:
            raise ValueError("Invalid tournament format.")

        print(f"Total matches: {total_matches}")  # Debugging

        total_duration = total_matches * match_duration
        print(f"Total duration (minutes): {total_duration}")  # Debugging

        return math.ceil(total_duration / (8 * 60))  # Assuming 8 hours per day

    def create_schedule(self, sport, num_teams, format, specific_days, schedule_format):
        total_days = self.calculate_duration(sport, num_teams, format)
        print(f"Total days calculated: {total_days}")  # Debugging
        schedule = []
        current_date = self.date  # Use the provided date

        if schedule_format == "consecutive":
            schedule = [self.date + timedelta(days=i) for i in range(total_days)]
        elif schedule_format == "specific_days":
            if not specific_days:
                raise ValueError("Specific days must be provided for 'specific_days' format.")
            while len(schedule) < total_days:
                if current_date.weekday() in specific_days:
                    schedule.append(current_date)
                current_date += timedelta(days=1)
            if len(schedule) < total_days:
                raise ValueError("Not enough specific days to schedule the tournament.")
        elif schedule_format == "custom_intervals":
            interval = 2  # Example: every 2 days
            for i in range(total_days):
                schedule.append(self.date + timedelta(days=i * interval))
        else:
            raise ValueError(f"Invalid schedule format: {schedule_format}")

        print(f"Generated schedule: {schedule}")  # Debugging
        return schedule