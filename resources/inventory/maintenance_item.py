from .item import Item

class MaintenanceItem(Item):
    def __init__(self, name, maintenance_type, total_quantity=0):
        super().__init__(name, total_quantity=0)
        self.maintenance_type = maintenance_type
        self.total_quantity = total_quantity

    def __repr__(self):
        return f"{self.name} (Type: {self.maintenance_type}, Quantity: {self.total_quantity})"