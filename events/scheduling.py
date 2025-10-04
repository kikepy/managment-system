import os
import json
from datetime import datetime

SCHEDULE_FILE = "data/example_data.json"

def save_schedule_to_file(schedule):
    os.makedirs(os.path.dirname(SCHEDULE_FILE), exist_ok=True)
    with open(SCHEDULE_FILE, "w") as file:
        json.dump(schedule, file, default=str)

def load_schedule_from_file():
    try:
        if os.path.exists(SCHEDULE_FILE) and os.path.getsize(SCHEDULE_FILE) > 0:
            with open(SCHEDULE_FILE, "r") as file:
                schedule = json.load(file)
                for event in schedule:
                    try:
                        event["start"] = datetime.fromisoformat(event["start"])
                        event["end"] = datetime.fromisoformat(event["end"])
                    except ValueError:
                        raise ValueError(f"Invalid date format in event: {event}")
                return schedule
        else:
            # Return an empty list if the file does not exist or is empty
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")