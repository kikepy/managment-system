# File: events/scheduling.py

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
        with open(SCHEDULE_FILE, "r") as file:
            schedule = json.load(file)
            for event in schedule:
                try:
                    event["start"] = datetime.fromisoformat(event["start"])
                    event["end"] = datetime.fromisoformat(event["end"])
                except ValueError:
                    raise ValueError(f"Invalid date format in event: {event}")
            return schedule
    except FileNotFoundError:
        return []