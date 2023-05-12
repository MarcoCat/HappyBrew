import csv
import os
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from database import db
from models import Order, Product, ProductsOrder, User


def create_db(product_file):
    with app.app_context():
        db.create_all()
        print("Create all tables successfully.")

        with open(product_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            next(reader)
            for row in reader:
                obj = Product(
                    name=row[0],
                    price=float(row[1]),
                    category=row[2],
                    description=row[3],
                    quantity=int(row[4]),
                )
                db.session.add(obj)
        db.session.commit()
        print("Successfully created all products.")


app = Flask(__name__)
app.instance_path = str(Path(".").resolve())
app.secret_key = "abcdefg"

if __name__ == "__main__":
    DB_NAME = "store"
else:
    DB_NAME = "test"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}.db"

login_manager = LoginManager(app)
app.instance_path = str(Path(".").resolve())
db.init_app(app)

if not os.path.isfile(f"{DB_NAME}.db") and DB_NAME == "store":
    create_db("products.csv")

if DB_NAME == "test":
    create_db("test_products.csv")

app.secret_key = "abcdefg"


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/menu")
def index():
    products = Product.query.all()
    categories = sorted(list(set([product.category for product in products])))
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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if not user:
            return render_template("login.html", error="Username not found")

        elif user.password != password:
            return render_template("login.html", error="Incorrect password")

        else:
            login_user(user)
            return redirect("dashboard")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # extract user data from form
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        user_exists = User.query.filter_by(username=username).first()

        if user_exists:
            return render_template("signup.html", error="Username already taken")

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")


@app.route("/dashboard")
def test_login():
    if current_user.is_authenticated:
        return render_template("dashboard.html", user=current_user)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/customize")
def customize():
    return render_template("customize1.html")


@app.route("/cart", defaults={"order_id": None})
@app.route("/cart/<int:order_id>")
def cart(order_id=None):
    def calculate_total(orders):
        return sum(order.total_price for order in orders)

    if order_id:
        orders = [db.session.get(Order, order_id)]
    else:
        orders = Order.query.all()
    if not orders:
        return "Order not found", 404
    total = calculate_total(orders)
    return render_template("cart.html", orders=orders, total=total)


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


@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


if __name__ == "__main__":
    app.run()
