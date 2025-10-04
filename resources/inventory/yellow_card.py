from .item import Item

class Yellow(Item):
    def __init__(self, quantity = 0):
        super().__init__("Yellow Card")
        self.total_quantity = quantity