from .staff import Staff

class Doctor(Staff):
    def __init__(self, name, specialization, certification, availability=True):
        super().__init__(name, "Doctor", availability)
        self.specialization = specialization
        self.certification = certification

    def __repr__(self):
        status = "Available" if self.availability else "Unavailable"
        return f"{self.role}: {self.name}, Specialization: {self.specialization}, Certification: {self.certification}, {status}"