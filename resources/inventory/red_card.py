from .item import Item

class Red(Item):
    def __init__(self, total_quantity=0):
        super().__init__("Red Card", total_quantity=0)
        self.total_quantity = total_quantity