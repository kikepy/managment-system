from .event import Event
from datetime import datetime
from .event import Event
class Training(Event):
    def __init__(self, name, date, location, sport, duration):
        super().__init__(name, date, location, sport, event_type="training")
        self.duration = duration

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date.isoformat(),
            "location": self.location,
            "sport": self.sport,
            "event_type": self.event_type,
            "duration": self.duration,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            date=datetime.fromisoformat(data["date"]),
            location=data["location"],
            sport=data["sport"],
            duration=data["duration"],
        )