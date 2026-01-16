from datetime import datetime

def flatten_tournament_schedules(events):
    flattened = []
    for event in events:
        if event.get("event_info", {}).get("type") == "tournament":
            flattened.extend(event.get("schedule", []))  # Add all matches in the tournament
        else:
            flattened.append(event)  # Add regular events
    return flattened

def get_attr(event, attr):
    # Handle dictionaries
    if isinstance(event, dict):
        event_type = event.get("event_info", {}).get("type", "").lower()
        if event_type == "tournament" and attr in ["start", "end", "location"]:
            raise ValueError(f"Cannot directly access '{attr}' for a tournament. Use nested schedules.")
        if attr == "event_type":
            return event.get("event_info", {}).get("type")
        elif attr == "start":
            start = event.get("schedule", {}).get("start")
            return datetime.fromisoformat(start) if start else None
        elif attr == "end":
            end = event.get("schedule", {}).get("end")
            return datetime.fromisoformat(end) if end else None
        elif attr == "location":
            return event.get("schedule", {}).get("location")
        elif attr == "name":
            return event.get("event_info", {}).get("name")

    # Handle objects
    return getattr(event, attr, None)
def validate_no_overlap(new_event, existing_events):
    # Flatten all tournament schedules
    all_events = flatten_tournament_schedules(existing_events)

    # Check for overlaps
    for event in all_events:
        # Handle both objects and dictionaries
        event_location = event["schedule"]["location"] if isinstance(event, dict) else event.location
        new_event_location = new_event["schedule"]["location"] if isinstance(new_event, dict) else new_event.location

        if event_location == new_event_location:
            existing_start = datetime.fromisoformat(event["schedule"]["start"]) if isinstance(event, dict) else event.start
            existing_end = datetime.fromisoformat(event["schedule"]["end"]) if isinstance(event, dict) else event.end
            new_start = datetime.fromisoformat(new_event["schedule"]["start"]) if isinstance(new_event, dict) else new_event.start
            new_end = datetime.fromisoformat(new_event["schedule"]["end"]) if isinstance(new_event, dict) else new_event.end

            # Check if the events overlap
            if not (new_end <= existing_start or new_start >= existing_end):
                raise ValueError("Event overlaps with an existing event at the same location.")

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

def validate_event(event, available_items, available_staff, existing_events, allow_past_events=False):
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

    inventory = {
        "items": [{"type": item, "total_quantity": quantity} for item, quantity in available_items.items()],
        "staff": [{"role": role, "availability": availability} for role, availability in available_staff.items()]
    }

    # Validate required items for the event
    validate_items(event.REQUIRED_ITEMS, available_items)

    # Validate required staff for the event
    validate_staff(event.REQUIRED_STAFF, available_staff, inventory)

    # Validate no overlap with existing events
    validate_no_overlap(event, existing_events)
    if not allow_past_events:
        event_start = event.start
        current_date = datetime.now()
        if event_start < current_date:
            raise ValueError("Match date cannot be in the past.")

    # Event-specific validations
    if event.event_type == "friendly":
        if len(event.teams) != 2:
            raise ValueError("Friendly matches must have exactly two teams.")
    elif event.event_type == "official":
        if "level" not in event.referee or event.referee["level"] != "high":
            raise ValueError("Official matches require a referee with a 'high' level.")
        if len(event.commentators) < 2:
            raise ValueError("Official matches must have at least two commentators.")
    elif event.event_type == "tournament":
        if len(event.teams) < 4:
            raise ValueError("Tournaments must have at least four teams.")
        if event.format not in ["knockout", "round-robin", "mixed"]:
            raise ValueError("Invalid tournament format. Must be 'knockout', 'round-robin', or 'mixed'.")
        if not event.specific_days:
            raise ValueError("Tournaments must have specific days defined.")
    elif event.event_type == "training":
        if not event.coach:
            raise ValueError("Training events must have a coach assigned.")
    else:
        raise ValueError(f"Unknown event type: {event.event_type}")