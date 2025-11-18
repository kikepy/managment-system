from .event import Event
from .validation import validate_tournament
from datetime import datetime, timedelta

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
        random.shuffle(teams)  # Shuffle teams for random pairing in the first round

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
            # Placeholder: Winners advance to the next round (to be determined later)
            teams = ["Winner of " + match["event_info"]["name"] for match in round_matches]
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

    def _generate_schedule(self):
        matches = []
        if self.format == "knockout":
            matches = self._create_knockout_matches()
        elif self.format == "round-robin":
            matches = self._create_league_matches()

        scheduled_matches = []
        day_index = 0
        match_start_times = [
            (7, 0),  # 7:00 AM
            (9, 0),  # 9:00 AM
            (13, 30),  # 1:30 PM
            (16, 0)  # 4:00 PM
        ]

        for match in matches:
            if day_index >= len(self.specific_days):
                day_index = len(self.specific_days) - 1  # Use the last day if out of days

            # Assign the next available time slot
            for start_hour, start_minute in match_start_times:
                start_time = self.specific_days[day_index].replace(hour=start_hour, minute=start_minute)
                end_time = start_time + timedelta(hours=1, minutes=30)  # Match duration: 1.5 hours

                scheduled_matches.append({
                    "round": match["round"],
                    "teams": match["teams"],
                    "schedule": {
                        "start": start_time.isoformat(),
                        "end": end_time.isoformat(),
                        "location" : "Stadium A" #Default
                    },
                    "event_info": match["event_info"]
                })

                # Move to the next time slot
                match_start_times.remove((start_hour, start_minute))
                if not match_start_times:  # If no time slots are left, move to the next day
                    match_start_times = [
                        (7, 0), (9, 0), (13, 30), (16, 0)
                    ]
                    day_index += 1
                break

        return scheduled_matches

    def to_dict(self):
        if not self.schedule:
            self.schedule = self._generate_schedule()
        return {
            "event_info": {
                "name": self.name,
                "sport": self.sport,
                "type": "tournament"
            },
            "teams": self.teams,
            "format": self.format,
            "specific_days": [day.strftime('%Y-%m-%d') for day in self.specific_days],
            "schedule": self.schedule,
            "sources": {
                "items": self.REQUIRED_ITEMS,
                "staff": self.REQUIRED_STAFF
            }
        }

    @classmethod
    def from_dict(cls, data):
        # Filter out invalid schedules with TBD values
        valid_schedule = [
            match for match in data["schedule"]
            if match["schedule"].get("start") != "TBD" and match["schedule"].get("end") != "TBD"
        ]

        if not valid_schedule:
            raise ValueError("No valid schedule found for the tournament.")

        instance = cls(
            name=data["event_info"]["name"],
            date=datetime.fromisoformat(valid_schedule[0]["schedule"]["start"]),
            location=valid_schedule[0].get("location", "Unknown"),
            sport=data["event_info"]["sport"],
            teams=data["teams"],
            format=data["format"],
            specific_days=[datetime.fromisoformat(day) for day in data["specific_days"]]
        )
        return instance