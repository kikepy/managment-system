from .item import Item

class SellerProduct(Item):
    def __init__(self, product_name, price, total_quantity=0):
        super().__init__(product_name, total_quantity=0)
        self.price = price
        self.total_quantity = total_quantity

    def __repr__(self):
        return f"{self.name} (Price: ${self.price}, Quantity: {self.total_quantity})"