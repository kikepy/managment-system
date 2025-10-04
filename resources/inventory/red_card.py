from .item import Item

class Red(Item):
    def __init__(self, quantity = 0):
        super().__init__("Red Card")
        self.quantity = quantity