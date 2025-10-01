#Main class for manage the inventory in the stadium
from .balls import Ball
class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity=1):
        item.total_quantity += quantity
        self.items.append(item)

    def remove_item(self, item, quantity=1):
        if item.total_quantity >= quantity:
            item.total_quantity -= quantity
            if item.total_quantity == 0:
                self.items.remove(item)
        else:
            raise ValueError("Not enough quantity to remove")

    def list_items(self):
        return [str(item) for item in self.items]

    #Helper method to count the balls by sport
    def count_balls_by_sport(self):
        ball_counts = {}
        for item in self.items:
            if isinstance(item, Ball):
                if item.sport not in ball_counts:
                    ball_counts[item.sport] = 0
                ball_counts[item.sport] += item.total_quantity
        return ball_counts

    #Find items by name
    def find_item_by_name(self, name):
        return [item for item in self.items if item.name == name]