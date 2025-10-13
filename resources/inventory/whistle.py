from .item import Item

class Whistle(Item):
    def __init__(self, total_quantity=0):
        super().__init__("Whistle", total_quantity=0)
        self.total_quantity = total_quantity