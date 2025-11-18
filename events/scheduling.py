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
        with open("events.json", "r") as file:
            data = json.load(file)

        events = []
        for event_type, event_list in data.items():
            for event in event_list:
                # Extract event_type from event_info if not directly available
                event_type = event.get("event_type") or event["event_info"].get("type")
                if not event_type:
                    print(f"Skipping event due to missing 'event_type': {event}")
                    continue

                if event_type in EVENT_CLASSES:
                    try:
                        events.append(EVENT_CLASSES[event_type].from_dict(event))
                    except Exception as e:
                        print(f"Error processing event: {event}. Error: {e}")
                else:
                    print(f"Unknown event type: {event_type}")
        return events
    except FileNotFoundError:
        print("Schedule file not found.")
        return []
    except Exception as e:
        print(f"Error loading schedule: {e}")
        return []