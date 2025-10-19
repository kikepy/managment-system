from .staff import Staff
class Commentator(Staff):
    Commentators_by_sport = {
        "futsal": 2,
        "basketball": 2,
        "volleyball": 2
    }

    def __init__(self, name, languages, experience_years, aviability=True):
        super().__init__(name, "Commentator")
        self.languages = languages
        self.experience_years = experience_years
        self.required_items = {"microphone": 1}

    def assign_microphones(self, available_microphones):
        if available_microphones >= self.required_items["microphone"]:
            available_microphones -= self.required_items["microphone"]
            print(f"Microphone assigned to {self.name}. Remaining microphones: {available_microphones}")
        else:
            print(f"Not enough microphones for {self.name}. Required: {self.required_items['microphone']}, Available: {available_microphones}")
        return available_microphones


    def __repr__(self):
        status = "Available" if self.availability else "Unavailable"
        return f"{self.role}: {self.name}, Languages: {', '.join(self.languages)}, Experience: {self.experience_years} years, {status}"