from .event import Event
from .validation import validate_tournament
from datetime import datetime

class Tournament(Event):
    REQUIRED_ITEMS = {"Ball": 4}
    REQUIRED_STAFF = {"Referee": 2, "Commentator": 1}

    def __init__(self, name, date, location, sport, teams, format, specific_days):
        validate_tournament(teams, format, date, specific_days)
        super().__init__(name, date, location, sport, event_type="tournament")
        self.teams = teams
        self.format = format
        self.specific_days = specific_days
        self.schedule = []

    def _create_knockout_matches(self):
        import random
        matches = []
        teams = self.teams.copy()
        random.shuffle(teams)

        round_num = 1
        while len(teams) > 1:
            round_matches = []
            for i in range(0, len(teams), 2):
                if i + 1 < len(teams):
                    match = {
                        "round": round_num,
                        "teams": {
                            "home": teams[i],
                            "away": teams[i + 1]
                        },
                        "event_info": {
                            "name": f"Round {round_num} - Match {len(round_matches) + 1}",
                            "sport": self.sport,
                            "type": "tournament"
                        }
                    }
                    round_matches.append(match)

            matches.extend(round_matches)
            teams = teams[::2]  # Winners advance (placeholder)
            round_num += 1

        return matches

    def _create_league_matches(self):
        matches = []
        match_num = 1

        for i, team1 in enumerate(self.teams):
            for team2 in self.teams[i + 1:]:
                match = {
                    "round": 1,
                    "teams": {
                        "home": team1,
                        "away": team2
                    },
                    "event_info": {
                        "name": f"League Match {match_num}",
                        "sport": self.sport,
                        "type": "tournament"
                    }
                }
                matches.append(match)
                match_num += 1

        return matches

    def to_dict(self):
        return {
            "event_info": {
                "name": self.name,
                "sport": self.sport,
                "type": "tournament"
            },
            "teams": self.teams,
            "format": self.format,
            "specific_days": [day.strftime('%Y-%m-%d') for day in self.specific_days],
            "schedule": [],  # Empty schedule for now
            "sources": {
                "items": self.REQUIRED_ITEMS,
                "staff": self.REQUIRED_STAFF
            }
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            name=data["event_info"]["name"],
            date=datetime.fromisoformat(data["matches"][0]["schedule"]["start"]),
            location=data["matches"][0]["schedule"]["location"],
            sport=data["event_info"]["sport"],
            teams=data["teams"],
            format=data["format"],
            specific_days=[datetime.fromisoformat(day) for day in data["specific_days"]]
        )
        return instance