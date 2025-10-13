from .item import Item
class Ball(Item):
    def __init__(self, sport, total_quantity=0):
        super().__init__("Ball", total_quantity=0)
        self.sport = sport
        self.total_quantity = total_quantity
        

    def __repr__(self):
        return f"Ball ({self.sport.capitalize()}):{self.total_quantity}"