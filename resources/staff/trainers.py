from .staff import Staff

class Trainer(Staff):
    def __init__(self, name, sport, availability):
        super().__init__(name, "Trainer", availability)
        self.sport = sport

    def __repr__(self):
        status = "Available" if self.availability else "Unavailable"
        return f"Name: {self.name} Role: {self.role} Sport: {self.sport}, {status}"
