from .event import Event
from datetime import datetime

class FriendlyMatch(Event):
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
            date=datetime.fromisoformat(data["start"]), # Use "start" to match Event's attribute
            location=data["location"],
            sport=data["sport"],
            teams=data["teams"],
        )