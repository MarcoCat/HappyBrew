import json
from pathlib import Path

from database import db
from flask import Flask, jsonify, redirect, render_template, request, url_for
from models import Order, Product, ProductsOrder

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.instance_path = str(Path(".").resolve())
db.init_app(app)

with open("menu.json") as f:
    menu = json.load(f)

orders = []


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/menu")
def index():
    with open("menu.json") as f:
        menu = json.load(f)
    return render_template("menu.html", menu=menu)


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
    if orders:
        return render_template("cart.html", orders=orders)
    else:
        return "Your cart is empty."


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/order")
def order():
    return render_template("order.html", menu=menu)


@app.route("/order", methods=["POST"])
def create_order():
    form_data = request.form.to_dict()
    print(form_data)
    data = {"name": form_data["name"], "address": form_data["address"], "products": []}
    for i in range(len(form_data) // 2 - 1):
        product = {
            "name": form_data[f"products[{i}][name]"],
            "quantity": int(form_data[f"products[{i}][quantity]"]),
        }
        data["products"].append(product)
    print(data)

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


if __name__ == "__main__":
    app.run()
