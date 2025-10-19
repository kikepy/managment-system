import os
import json

SCHEDULE_FILE = "data/example_data.json"

def save_schedule_to_file(schedule):
    os.makedirs(os.path.dirname(SCHEDULE_FILE), exist_ok=True)
    with open(SCHEDULE_FILE, "w") as file:
        # Convert all event objects to dictionaries
        json.dump([event.to_dict() for event in schedule], file, default=str)

def load_schedule_from_file():
    from .friendly_match import FriendlyMatch
    from .official import OfficialMatch
    from .tournament import Tournament
    from .training import Training

    # Map event types to their respective classes
    EVENT_CLASSES = {
        "friendly": FriendlyMatch,
        "official": OfficialMatch,
        "tournament": Tournament,
        "training": Training,
    }


    try:
        with open(SCHEDULE_FILE, "r") as file:
            data = json.load(file)

        # Convert dictionaries to event objects based on their event_type
        return [
            EVENT_CLASSES[event["event_type"]].from_dict(event)
            for event in data
        ]
    except FileNotFoundError:
        return []
    except (ValueError, KeyError, TypeError) as e:
        print(f"Error loading schedule: {e}")
        return []