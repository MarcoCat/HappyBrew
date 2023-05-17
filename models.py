from flask_login import UserMixin

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


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    products = db.relationship("ProductsOrder", back_populates="order")

    @property
    def total_price(self):
        if not self.products:
            return 0
        return round(
            sum(product.product.price * product.quantity for product in self.products),
            2,
        )

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "products": [
                {
                    "name": product.product_name,
                    "quantity": product.quantity,
                }
                for product in self.products
            ],
            "price": self.total_price,
        }

    def process(self):
        if self.completed:
            return

        for product_order in self.products:
            product = product_order.product
            if product.quantity < product_order.quantity:
                product_order.quantity = product.quantity
            product.quantity -= product_order.quantity

        self.completed = True
        db.session.commit()


class ProductsOrder(db.Model):
    product_name = db.Column(db.ForeignKey("product.name"), primary_key=True)
    order_id = db.Column(db.ForeignKey("order.id"), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship("Product")
    order = db.relationship("Order", back_populates="products")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)


class Custom_Product(db.Model):
    name = db.Column(db.String, unique=True, primary_key=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    ingredients = db.relationship(
        "Ingredient", secondary="product_ingredient", backref="products"
    )
