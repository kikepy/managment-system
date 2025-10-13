class Staff:
    def __init__(self, name, role, availability=True):
        self.name = name
        self.role = role
        self.availability = availability

    # Helper method to return the availability
    def is_available(self) -> bool:
        return self.availability

    def __repr__(self):
        status = "Available" if self.availability else "Unavailable"
        return f"{self.name}, {self.role}, {status}"

