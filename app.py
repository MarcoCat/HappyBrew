from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user

from database import db
from models import Order, Product, ProductsOrder, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.instance_path = str(Path(".").resolve())
db.init_app(app)

login_manager = LoginManager(app)
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
            return redirect("test_login")

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


@login_required
@app.route("/test_login")
def test_login():
    return render_template("test_login.html", user=current_user)


@app.route("/customize")
def customize():
    return render_template("customize1.html")


@app.route("/cart", defaults={"order_id": None})
@app.route("/cart/<int:order_id>")
def cart(order_id=None):
    if order_id:
        order = db.session.get(Order, order_id)
        if not order:
            return "Order not found", 404
        return render_template("cart.html", orders=[order])
    else:
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
