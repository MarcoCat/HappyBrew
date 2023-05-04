from database import db


class Product(db.Model):
    name = db.Column(db.String, unique=True, primary_key=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "description": self.description,
            "quantity": self.quantity,
        }
