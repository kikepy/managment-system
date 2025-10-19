from .item import Item

class Speaker(Item):
    def __init__(self, total_quantity=0,is_broken = False):
        super().__init__("Speaker")
        self.is_broken = is_broken
        self.total_quantity = total_quantity

    def __repr__(self):
        return f"{self.name}: {self.total_quantity})"