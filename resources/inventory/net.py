from functools import total_ordering

from .item import Item

class Net(Item):
    def __init__(self, total_quantity=0):
        super().__init__("Net", total_quantity=0)

        self.total_quantity = total_quantity

    def __repr__(self):
        return f"{self.name}:  {self.total_quantity}"