from .staff import Staff

class Seller(Staff):
    def __init__(self, name, sales_experience, products, availability=True):
        super().__init__(name, "Seller", availability)
        self.sales_experience = sales_experience
        self.products = products
        self.required_items = {"Products": len(products)}

    def __repr__(self):
        status= "Available" if self.availability else "Unavailable"
        return f"{self.role}: {self.name}, Experience: {self.sales_experience} years, Products: {self.products}, {status}"