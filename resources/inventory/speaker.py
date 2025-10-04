from .item import Item

class Speaker(Item):
    def __init__(self, quantity = 0,is_broken = False):
        super().__init__("Speaker")
        self.is_broken = is_broken
        self.total_quantity = quantity

    def __repr__(self):
        return f"{self.name} (Broken: {self.is_broken}, Quantity: {self.total_quantity})"