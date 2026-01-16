#Main class to represent an event with attributes like name, date, location, and duration.
#The duration will be displayed in min
from datetime import timedelta
from resources.dependency_checker import check_dependencies
from datetime import datetime

class Event:
    match_durations = {
        "futsal": {"periods": [20, 10, 20], "extra_time": 10},
        "basketball": {"periods": [12, 12, 12, 12], "extra_time": 5},
        "volleyball": {"periods": [25, 25, 25], "extra_time": 5},

    }

    required_items = {
        "futsal": {"balls": 2},
        "basketball": {"balls": 2},
        "volleyball": {"net": 1, "balls": 2},

    }

    required_staff = {
        "friendly": {"referee": 1, "assistant_referees": 2},
        "official": {"referee": 1, "assistant_referees": 2, "commentators": 2},
        "training": {"trainer": 1},
        "tournament": {"referee": 2, "assistant_referees": 4, "commentators": 2, "organizers": 1},
    }
    def __init__(self, name, start, location, sport, event_type):
        self.name = name
        self.start = start
        self.location = location
        self.sport = sport
        self.event_type = event_type
        self.duration = self.calculate_total_duration(sport)
        self.end = self.calculate_end_time()

    @classmethod
    def calculate_total_duration(cls, sport):
        sport_durations = {
            "soccer": 90,
            "basketball": 48,
            "volleyball": 60,
        }
        return sport_durations.get(sport.lower(), 0)

    def calculate_end_time(self):
        return self.start + timedelta(minutes=self.duration)

    def to_dict(self):
        return {
            "name": self.name,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "location": self.location,
            "sport": self.sport,
            "event_type": self.event_type,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            start=datetime.fromisoformat(data["start"]),
            location=data["location"],
            sport=data["sport"],
            event_type=data["event_type"],
        )

    def __repr__(self):
        return (
            f"{self.name} (Start: {self.start}, End: {self.end}, Location: {self.location}, "
            f"Sport: {self.sport}, Event Type: {self.event_type}, Duration: {self.duration} minutes)"
        )