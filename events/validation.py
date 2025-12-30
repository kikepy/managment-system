from datetime import datetime

def validate_no_overlap(new_event, existing_events):
    # Collect tournament days
    tournament_days = set()
    for event in existing_events:
        if event.event_type == "tournament":
            # Extract days from the schedule
            if hasattr(event, 'schedule') and event.schedule:
                for match in event.schedule:
                    if isinstance(match, dict) and 'schedule' in match and 'start' in match['schedule']:
                        match_date = datetime.fromisoformat(match['schedule']['start']).date()
                        tournament_days.add(match_date)
            # Extract specific days
            if hasattr(event, 'specific_days'):
                for day in event.specific_days:
                    if isinstance(day, str):
                        tournament_days.add(datetime.strptime(day, '%Y-%m-%d').date())
                    else:
                        tournament_days.add(day.date())

    # Check if the new event falls on a tournament day
    if new_event.event_type != "tournament":
        new_event_date = new_event.start.date()
        if new_event_date in tournament_days:
            raise ValueError(f"Cannot create event on {new_event_date} as it is reserved for a tournament.")

    # Check for time and location overlap
    for event in existing_events:
        if not all(hasattr(event, attr) for attr in ['location', 'start', 'end']):
            continue  # Skip events missing required attributes

        if event.location == new_event.location:
            if not (new_event.end <= event.start or new_event.start >= event.end):
                raise ValueError(
                    f"Overlap detected with event '{event.name}' at {event.location} "
                    f"from {event.start} to {event.end}."
                )



def validate_date(event_date, event_type):
    try:
        # Ensure the date is a valid datetime object
        parsed_date = datetime.fromisoformat(event_date)
    except ValueError:
        raise ValueError(f"Invalid date format: {event_date}. Expected ISO format (YYYY-MM-DD HH:MM:SS).")

    # Check if the date is in the past
    if event_type != "tournament" and parsed_date < datetime.now():
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
    if not specific_days:
        raise ValueError("Tournament must have specific days defined.")

def validate_training(date, coach, required_items, available_items):
    # Validate the date
    if not isinstance(date, datetime):
        raise ValueError("Invalid date format. Expected a datetime object.")
    if date < datetime.now():
        raise ValueError("Training date cannot be in the past.")

    # Validate the coach
    if not coach or not isinstance(coach, str):
        raise ValueError("A valid coach must be provided.")

    # Validate required items for training
    for item, quantity in required_items.items():
        available_quantity = available_items.get(item, 0)
        if available_quantity < quantity:
            raise ValueError(
                f"Missing required item: {item}. Required: {quantity}, Available: {available_quantity}"
            )

def validate_items(required_items, available_items):
    for item, quantity in required_items.items():
        available_quantity = available_items.get(item, 0)
        if available_quantity < quantity:
            raise ValueError(
                f"Missing required item: {item}. Required: {quantity}, Available: {available_quantity}"
            )

def validate_staff(required_staff, available_staff, inventory):
    for role, count in required_staff.items():
        if available_staff.get(role, 0) < count:
            raise ValueError(
                f"Insufficient staff for role '{role}'. Required: {count}, Available: {available_staff.get(role, 0)}"
            )
    #Validate by the items that they need
    available_items = {item["type"]: item["total_quantity"] for item in inventory["items"]}
    for staff in inventory["staff"]:
        role = staff["role"]
        if hasattr(globals().get(role, None), "REQUIRED_ITEMS"):
            required_items = globals()[role].REQUIRED_ITEMS
            validate_items(required_items, available_items)

def validate_event(event, available_items, available_staff, existing_events):
    """
    Centralized validation function for all event types.

    Args:
        event: The event object to validate.
        available_items: A dictionary of available items and their quantities.
        available_staff: A dictionary of available staff and their availability.
        existing_events: A list of existing events to check for overlaps.

    Raises:
        ValueError: If any validation fails.
    """
    # Validate required items for the event
    validate_items(event.REQUIRED_ITEMS, available_items)

    # Validate required staff for the event
    validate_staff(event.REQUIRED_STAFF, available_staff)

    # Validate no overlap with existing events
    validate_no_overlap(event, existing_events)

    # Event-specific validations
    if event.event_type == "Friendly":
        if len(event.teams) != 2:
            raise ValueError("Friendly matches must have exactly two teams.")
    elif event.event_type == "Official":
        if "level" not in event.referee or event.referee["level"] != "high":
            raise ValueError("Official matches require a referee with a 'high' level.")
        if len(event.commentators) < 2:
            raise ValueError("Official matches must have at least two commentators.")
    elif event.event_type == "Tournament":
        if len(event.teams) < 4:
            raise ValueError("Tournaments must have at least four teams.")
        if event.format not in ["knockout", "round-robin", "mixed"]:
            raise ValueError("Invalid tournament format. Must be 'knockout', 'round-robin', or 'mixed'.")
        if not event.specific_days:
            raise ValueError("Tournaments must have specific days defined.")
    elif event.event_type == "Training":
        if not event.coach:
            raise ValueError("Training events must have a coach assigned.")
    else:
        raise ValueError(f"Unknown event type: {event.event_type}")