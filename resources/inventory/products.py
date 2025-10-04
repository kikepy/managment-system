from .item import Item

class SellerProduct(Item):
    def __init__(self, product_name, price, quantity = 0):
        super().__init__(product_name)
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"{self.name} (Price: ${self.price}, Quantity: {self.quantity})"