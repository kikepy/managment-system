import os
import json

SCHEDULE_FILE = "events.json"
print("Current working directory:", os.getcwd())
print("Expected file path:", os.path.abspath("events.json"))

def save_schedule_to_file(schedule):
    os.makedirs(os.path.dirname(SCHEDULE_FILE), exist_ok=True)
    with open(SCHEDULE_FILE, "w") as file:
        # Convert all event objects to dictionaries
        json.dump([event.to_dict() for event in schedule], file, default=str)

def load_schedule_from_file():
    from events.friendly_match import FriendlyMatch
    from events.official import OfficialMatch
    from events.tournament import Tournament
    from events.training import Training

    EVENT_CLASSES = {
        "friendly": FriendlyMatch,
        "official": OfficialMatch,
        "tournament": Tournament,
        "training": Training,
    }

    try:
        with open("events.json", "r") as file:  # Corrected path
            data = json.load(file)

        events = []
        for event_type, event_list in data.items():
            for event in event_list:
                if event["event_type"] in EVENT_CLASSES:
                    events.append(EVENT_CLASSES[event["event_type"]].from_dict(event))
        print(events)
        return events
    except FileNotFoundError:
        print("Schedule file not found.")
        return []
    except Exception as e:
        print(f"Error loading schedule: {e}")
        return []