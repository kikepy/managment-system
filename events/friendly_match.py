from .event import Event
from datetime import datetime
from datetime import timedelta


class FriendlyMatch(Event):
    REQUIRED_ITEMS = {"Ball" : 2}
    REQUIRED_STAFF = {"Referee" : 1}
    def __init__(self, name, date, location, sport, teams):
        from .validation import validate_friendly  # Local import to avoid circular dependency
        validate_friendly(date=date, teams=teams)
        super().__init__(name, date, location, sport, event_type="friendly")  # Pass `date` as `start`
        self.teams = teams
        self.end = date + timedelta(minutes=90)


    def to_dict(self):
        return {
            "event_info": {
                "name": self.name,
                "sport": self.sport,
                "type": "friendly"
            },
            "schedule": {
                "start": self.start.isoformat(),
                "end": self.end.isoformat(),
                "location": self.location
            },
            "teams": {
                "home": self.teams[0],
                "away": self.teams[1]
            },
            "resources": {
                "items": self.REQUIRED_ITEMS,
                "staff": self.REQUIRED_STAFF
            }
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            name=data["event_info"]["name"],
            date=datetime.fromisoformat(data["schedule"]["start"]),
            location=data["schedule"]["location"],
            sport=data["event_info"]["sport"],
            teams=[data["teams"]["home"], data["teams"]["away"]]
        )
        instance.end = datetime.fromisoformat(data["schedule"]["end"])
        return instance

