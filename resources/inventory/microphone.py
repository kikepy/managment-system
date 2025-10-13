from .item import Item

class Microphone(Item):
    def __init__(self, total_quantity=0):
        super().__init__("Microphone", total_quantity=0)
        self.total_quantity = total_quantity