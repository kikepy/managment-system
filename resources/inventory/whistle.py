from .item import Item

class Whistle(Item):
    def __init__(self, quantity = 0):
        super().__init__("Whistle")
        self.total_quantity = quantity