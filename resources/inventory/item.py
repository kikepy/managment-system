# Base class for all items
class Item:
    def __init__(self, name):
        self.name = name
        self.total_quantity = 0

    def add(self, quantity):
        self.total_quantity += quantity

    def remove(self, quantity):
        if self.total_quantity >= quantity:
            self.total_quantity -= quantity
            return True
        return False

    def check_availability(self, quantity):
        return self.total_quantity >= quantity

    def __repr__(self):
        return f"{self.name}: {self.total_quantity}"


