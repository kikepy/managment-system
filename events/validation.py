from datetime import datetime
from .scheduling import load_schedule_from_file


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