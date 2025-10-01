from .event import Event
from .validation import validate_friendly

class FriendlyMatch(Event):
    def __init__(self, name, date, location, sport, teams):
        validate_friendly(date=date, teams=teams)
        super().__init__(name, date, location, sport, event_type="friendly")
        self.teams = teams