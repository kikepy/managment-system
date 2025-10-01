from .event import Event
from .validation import validate_official

class OfficialMatch(Event):
    def __init__(self, name, date, location, sport, referee, competition, commentators):
        validate_official(date=date, referee=referee, commentators=commentators)
        super().__init__(name, date, location, sport, event_type="official")
        self.referee = referee
        self.competition = competition
        self.commentators = commentators