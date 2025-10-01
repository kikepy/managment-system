from .staff import Staff

class Maintenance(Staff):
    def __init__(self, name, skills, shift, availability=True, tools=None):
        super().__init__(name, "Maintenance", availability)
        self.skills = skills
        self.shift = shift
        self.required_items = {tool: 1 for tool in tools}
    def __repr__(self):
        status = "Available" if self.availability else "Unavailable"
        return f"{self.role}: {self.name}, Skills: {self.skills}, Shift: {self.shift}, {status}"