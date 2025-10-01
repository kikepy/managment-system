from .item import Item

class MaintenanceItem(Item):
    def __init__(self, item_name, maintenance_type):
        super().__init__(item_name)
        self.maintenance_type = maintenance_type

    def __repr__(self):
        return f"{self.name} (Type: {self.maintenance_type}, Quantity: {self.total_quantity})"