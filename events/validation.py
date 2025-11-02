from datetime import datetime
from resources import *

def validate_no_overlap(new_event, existing_events):
    for event in existing_events:
        # Check for overlap only if the locations are the same
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

def validate_tournament(teams, format, date):
    if not isinstance(date, datetime):
        raise ValueError("Invalid date format. Expected a datetime object.")
    if date < datetime.now():
        raise ValueError("Tournament date cannot be in the past.")
    if not isinstance(teams, list) or len(teams) < 4:
        raise ValueError("Tournaments must have at least four teams.")
    if format not in ["knockout", "round-robin", "mixed"]:
        raise ValueError("Invalid tournament format. Must be 'knockout', 'round-robin', or 'mixed'.")
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