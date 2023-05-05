import json
from pathlib import Path

from database import db
from flask import Flask, jsonify, redirect, render_template, request, url_for
from models import Order, Product, ProductsOrder

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.instance_path = str(Path(".").resolve())
db.init_app(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/menu")
def index():
    products = Product.query.all()
    categories = list(set([product.category for product in products]))
    product_dict = {}
    for category in categories:
        product_dict[category] = [
            product for product in products if product.category == category
        ]
    return render_template("menu.html", products=product_dict, categories=categories)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/instructions")
def contact():
    return render_template("instructions.html")


@app.route("/login")
def login():
    return render_template("loginsignup.html")


@app.route("/customize")
def customize():
    return render_template("customize1.html")


@app.route("/cart")
def cart():
    orders = Order.query.all()
    return render_template("cart.html", orders=orders)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/order")
def order():
    menu = Product.query.all()
    return render_template("order.html", menu=menu)


@app.route("/order", methods=["POST"])
def create_order():
    form_data = request.form.to_dict()
    data = {"name": form_data["name"], "address": form_data["address"], "products": []}
    for i in range(len(form_data) // 2 - 1):
        is_used = False
        for product in data["products"]:
            if product["name"] == form_data[f"products[{i}][name]"]:
                product["quantity"] += int(form_data[f"products[{i}][quantity]"])
                is_used = True
                break
        if not is_used:
            product = {
                "name": form_data[f"products[{i}][name]"],
                "quantity": int(form_data[f"products[{i}][quantity]"]),
            }
            data["products"].append(product)

    for key in ("name", "address", "products"):
        if key not in data:
            return f"The JSON is missing: {key}", 400

    for product in data["products"]:
        if not db.session.get(Product, product["name"]):
            return f"The product {product['name']} does not exist", 400

    order = Order(
        name=data["name"],
        address=data["address"],
    )

    for product in data["products"]:
        association = ProductsOrder(
            product=db.session.get(Product, product["name"]),
            order=order,
            quantity=product["quantity"],
        )
        db.session.add(association)
    db.session.add(order)
    db.session.commit()

    return redirect(url_for("cart"))


@app.route("/order/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return "Order not found", 404
    order_json = order.to_dict()
    return jsonify(order_json)


if __name__ == "__main__":
    app.run()
