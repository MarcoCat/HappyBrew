import json
from pathlib import Path

from database import db
from flask import Flask, jsonify, redirect, render_template, request, url_for
from models import Order, Product

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


# @app.route("/order", methods=["POST"])
# def process_order():
#     data = request.form.to_dict()
#     is_item_in_cart = False
#     for item in orders:
#         if item["item"] == data["item"]:
#             item["quantity"] = int(item["quantity"]) + int(data["quantity"])
#             is_item_in_cart = True
#     if not is_item_in_cart:
#         orders.append(data)
#     return redirect(url_for("cart"))


@app.route("/order", methods=["POST"])
def api_create_order():
    data = request.form.to_dict()
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

    return jsonify(order.to_dict())


@app.route("/order/<int:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        if order_id - 1 < 0:
            return "Order not found", 404
        return jsonify(orders[order_id - 1])
    except IndexError:
        return "Order not found", 404


if __name__ == "__main__":
    app.run()
