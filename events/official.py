from .event import Event
from datetime import datetime

class OfficialMatch(Event):
    def __init__(self, name, date, location, sport, referee, commentators):
        from .validation import validate_official  # Local import to avoid circular dependency
        validate_official(date=date, referee=referee, commentators=commentators)
        super().__init__(name, date, location, sport, event_type="official")
        self.referee = referee
        self.commentators = commentators

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date.isoformat(),
            "location": self.location,
            "sport": self.sport,
            "event_type": self.event_type,
            "referee": self.referee,
            "commentators": self.commentators,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            date=datetime.fromisoformat(data["date"]),
            location=data["location"],
            sport=data["sport"],
            referee=data["referee"],
            commentators=data["commentators"],
        )