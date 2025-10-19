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
            "tennis": 120,
            "volleyball": 60,
        }
        return sport_durations.get(sport.lower(), 0)

    def calculate_end_time(self):
        return self.start + timedelta(minutes=self.duration)

    @classmethod
    def validate_items_and_staff(cls, sport, event_type, available_items, available_staff, inventory):
        # Validate items
        required_items = cls.required_items.get(sport, {})
        for item, quantity in required_items.items():
            if available_items.get(item, 0) < quantity:
                raise ValueError(
                    f"Insufficient {item} for {sport}. Required: {quantity}, Available: {available_items.get(item, 0)}"
                )

        # Validate staff
        required_staff = cls.required_staff.get(event_type, {})
        for role, count in required_staff.items():
            if available_staff.get(role, 0) < count:
                raise ValueError(
                    f"Insufficient staff for role '{role}' in {event_type} event. Required: {count}, Available: {available_staff.get(role, 0)}"
                )

        # Check dependencies for staff
        staff_list = [
            {"role": role, "name": f"{role}_{i + 1}", "required_items": required_items}
            for role, count in required_staff.items()
            for i in range(count)
        ]
        if not check_dependencies(staff_list, inventory):
            raise ValueError("Staff dependencies validation failed.")

    def to_dict(self):
        return {
            "name": self.name,
            "start": self.start.isoformat(),
            "location": self.location,  # Ensure this is the stadium name
            "sport": self.sport,
            "event_type": self.event_type,
            "end": self.end.isoformat(),
            "required_items": self.required_items.get(self.sport.lower(), {}),  # Populate required items
            "required_staff": self.required_staff.get(self.event_type, {}),
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