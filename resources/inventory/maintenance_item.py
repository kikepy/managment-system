from .item import Item

class MaintenanceItem(Item):
    def __init__(self, item_name, maintenance_type, quantity = 0):
        super().__init__(item_name)
        self.maintenance_type = maintenance_type
        self.total_quantity = quantity

    def __repr__(self):
        return f"{self.name} (Type: {self.maintenance_type}, Quantity: {self.quantity})"