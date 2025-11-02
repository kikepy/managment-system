from .event import Event
from datetime import datetime
from resources.staff import *

class FriendlyMatch(Event):
    REQUIRED_ITEMS = {"Ball" : 2}
    REQUIRED_STAFF = {"Referee" : 1}
    def __init__(self, name, date, location, sport, teams):
        from .validation import validate_friendly  # Local import to avoid circular dependency
        validate_friendly(date=date, teams=teams)
        super().__init__(name, date, location, sport, event_type="friendly")  # Pass `date` as `start`
        self.teams = teams


    def to_dict(self):
        base_dict = super().to_dict()  # Get the base event details
        base_dict.update({
            "teams": self.teams,  # Add teams to the dictionary
        })
        return base_dict

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            date=datetime.fromisoformat(data["start"]),  # Convert ISO string to datetime
            location=data["location"],
            sport=data["sport"],
            teams=data["teams"]
        )