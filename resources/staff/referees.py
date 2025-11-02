from .staff import Staff

class Referee(Staff):
    #Dictionary to assign assistants by sport
    Assistants_by_sport = {
        "futsal" : 2,
        "basketball" : 1,
        "volleyball" : 2
    }

    REQUIRED_ITEMS = {
        "Whistle": 1,
        "Yellow Card": 1,
        "Red Card": 1
    }

    def __init__(self, name, sport, certification_level,assistants = None,availability=True):
        super().__init__(name, "Referee", availability)
        self.sport = sport
        self.certification_level = certification_level
        self.required_assistants = self.Assistants_by_sport.get(sport, 0)
        self.assistants = assistants if assistants else []


    def is_eligible_assistant(self, requester_certification) -> bool:
        if requester_certification == "high":
            return self.certification_level in ["mid", "low"]
        elif requester_certification == "mid":
            return self.certification_level in ["mid", "low"]
        return False

    @classmethod
    def assign_assistants(cls, referees):
        for referee in referees:
            if referee.certification_level in ["high", "mid"]:
                eligible_assistants = [
                    r.name for r in referees
                    if r.is_eligible_assistant(referee.certification_level)
                       and r.sport == referee.sport
                       and r.name != referee.name
                ]

                if len(eligible_assistants) < referee.required_assistants:
                    print(f"Not enough assistants for {referee.name} ({referee.sport}). Required: {referee.required_assistants}, Available: {len(eligible_assistants)}.")
                else:
                    referee.assistants.extend(eligible_assistants[:referee.required_assistants])

    def __repr__(self):
        status = "Available" if self.availability else "Unavailable"
        assistants = ", ".join(self.assistants) if self.assistants else "None"
        return f"{self.role}: {self.name}  Sport: {self.sport}, {self.certification_level} ,{status}"