import json

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

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
def process_order():
    data = request.form
    orders.append(data)
    return data


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
