# Base class for all items
class Item:
    def __init__(self, name, total_quantity=0):
        self.name = name
        self.total_quantity = total_quantity

    def add(self, total_quantity):
        self.total_quantity += total_quantity

    def remove(self, total_quantity):
        if self.total_quantity >= total_quantity:
            self.total_quantity -= total_quantity
            return True
        return False

    def check_availability(self, total_quantity):
        return self.total_quantity >= total_quantity

    def __repr__(self):
        return f"{self.name}: {self.total_quantity}"


