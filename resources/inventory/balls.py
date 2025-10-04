from .item import Item
class Ball(Item):
    def __init__(self, name, sport, total_quantity=0):
        super().__init__(name)
        self.sport = sport
        self.total_quantity = total_quantity
        

    def __str__(self):
        return f"{self.sport.capitalize()} Ball (Quantity: {self.total_quantity})"