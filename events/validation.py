from datetime import datetime
from resources import *
import json

def validate_no_overlap(new_event, existing_events):
    # Get tournament days from existing events
    tournament_days = set()
    for event in existing_events:
        if event.event_type == "tournament":
            # Handle case where schedule might be empty
            if hasattr(event, 'schedule') and event.schedule:
                for match in event.schedule:
                    # Check if match has the expected structure
                    if isinstance(match, dict) and 'schedule' in match and 'start' in match['schedule']:
                        match_date = datetime.fromisoformat(match['schedule']['start']).date()
                        tournament_days.add(match_date)
            # Also add the specific days from tournament
            if hasattr(event, 'specific_days'):
                for day in event.specific_days:
                    if isinstance(day, str):
                        tournament_days.add(datetime.strptime(day, '%Y-%m-%d').date())
                    else:
                        tournament_days.add(day.date())

    # Check if new event falls on a tournament day
    if new_event.event_type != "tournament":
        new_event_date = new_event.start.date()
        if new_event_date in tournament_days:
            raise ValueError(f"Cannot create event on {new_event_date} as it is reserved for a tournament.")

    # Check for time and location overlap with existing events
    for event in existing_events:
        # Skip if event doesn't have required attributes
        if not hasattr(event, 'location') or not hasattr(event, 'start') or not hasattr(event, 'end'):
            continue

        if event.location == new_event.location:
            if not (new_event.end <= event.start or new_event.start >= event.end):
                raise ValueError(
                    f"Overlap detected with event '{event.name}' at {event.location} "
                    f"from {event.start} to {event.end}."
                )



def validate_date(event_date):
    try:
        # Ensure the date is a valid datetime object
        parsed_date = datetime.fromisoformat(event_date)
    except ValueError:
        raise ValueError(f"Invalid date format: {event_date}. Expected ISO format (YYYY-MM-DD HH:MM:SS).")

    # Check if the date is in the past
    if parsed_date < datetime.now():
        raise ValueError(f"Event date {event_date} cannot be in the past.")

def validate_friendly(date, teams):
    if not isinstance(date, datetime):
        raise ValueError("Invalid date format. Expected a datetime object.")
    if date < datetime.now():
        raise ValueError("Match date cannot be in the past.")
    if not isinstance(teams, list) or len(teams) != 2:
        raise ValueError("Friendly matches must have exactly two teams.")
    if not all(isinstance(team, str) for team in teams):
        raise ValueError("Each team must be a string.")

def validate_official(date, referee, commentators):
    if not isinstance(date, datetime):
        raise ValueError("Invalid date format. Expected a datetime object.")
    if date < datetime.now():
        raise ValueError("Match date cannot be in the past.")
    if not isinstance(referee, dict) or "level" not in referee:
        raise ValueError("Referee must be a dictionary with a 'level' key.")
    if referee["level"] != "high":
        raise ValueError("Referee must have a 'high' level.")
    if not isinstance(commentators, list) or len(commentators) < 2:
        raise ValueError("There must be at least two commentators.")


def validate_tournament(teams, format, date, specific_days):
    if not isinstance(date, datetime):
        raise ValueError("Invalid date format. Expected a datetime object.")
    if date < datetime.now():
        raise ValueError("Tournament date cannot be in the past.")
    if not isinstance(teams, list) or len(teams) < 4:
        raise ValueError("Tournaments must have at least four teams.")
    if format not in ["knockout", "round-robin", "mixed"]:
        raise ValueError("Invalid tournament format. Must be 'knockout', 'round-robin', or 'mixed'.")

    # Validate specific days
    if not specific_days:
        raise ValueError("Tournament must have specific days defined")

    formatted_days = ', '.join(day.strftime('%Y-%m-%d') for day in specific_days)
    participating_teams = ', '.join(teams)
    print(f"Tournament starts on {formatted_days}. Teams participating: {participating_teams}.")
def validate_training():
    # Placeholder for training session validation logic
    pass


def validate_items(required_items, available_items):
    print("Validate items")
    for item, quantity in required_items.items():
        available_quantity = available_items.get(item, 0)  # Defaults to 0 if the item is missing
        print(f"Checking item: {item}, Required: {quantity}, Available: {available_quantity}")
        if available_quantity < quantity:
            raise ValueError(
                f"Missing required item: {item}. Required: {quantity}, Available: {available_quantity}"
            )

def validate_staff(required_staff, available_staff, inventory):
    print("Validate staff")
    for role, count in required_staff.items():
        if available_staff.get(role, 0) < count:
            raise ValueError(
                f"Insufficient staff for role '{role}'. Required: {count}, Available: {available_staff.get(role, 0)}"
            )
    available_items = {item["type"]: item["total_quantity"] for item in inventory["items"]}
    # Validate staff dependencies on items
    for staff in inventory["staff"]:
        if staff["role"] == "Referee":
            required_items = Referee.REQUIRED_ITEMS
            validate_items(required_items, available_items)