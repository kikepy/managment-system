from functools import total_ordering

from .item import Item

class Net(Item):
    def __init__(self, sport_type, quantity = 0):
        super().__init__("Net")
        self.sport_type = sport_type
        self.total_quantity = quantity

    def __repr__(self):
        return f"{self.name} (Sport: {self.sport_type}, Quantity: {self.total_quantity})"