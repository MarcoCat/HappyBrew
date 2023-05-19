import csv
import os
from pathlib import Path
import json

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from database import db
from models import (
    Feedback,
    Ingredient,
    Order,
    Product,
    ProductIngredient,
    ProductsOrder,
    User,
)


def create_db(product_file, ingredient_file):
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

        with open(ingredient_file, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            next(reader)
            for row in reader:
                obj = Ingredient(
                    name=row[0],
                    category=row[1],
                    description=row[2],
                    stock=int(row[3]),
                )
                db.session.add(obj)
        db.session.commit()
        print("Successfully created all ingredients.")


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
    create_db("products.csv", "ingredients.csv")

if DB_NAME == "test":
    create_db("test_products.csv", "ingredients.csv")

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


@app.route("/customize", methods=["POST"])
def create_drink():
    # sample json
    # {"name": "Good Drink", "ingredients": ["Aloe Vera", "Grass Jelly"], "description":"drink desc"}
    data = request.json
    name = data.get("name")
    ingredient_names = data.get("ingredients")
    description = data.get("description")

    if Product.query.filter_by(name=name).first():
        return jsonify({"error": "Product name already exists"}), 400

    product = Product(
        name=name, description=description, price=7.00, category="Custom", quantity=1
    )

    for ingredient_name in ingredient_names:
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if ingredient is None:
            return jsonify({"error": f"Ingredient '{ingredient_name}' not found"}), 400

        product.ingredients.append(ingredient)

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@app.route("/cart", defaults={"order_id": None})
@app.route("/cart/<int:order_id>")
def cart(order_id=None):
    def calculate_total(orders):
        return sum(order.total_price for order in orders)

    if order_id:
        orders = [db.session.get(Order, order_id)]
    else:
        orders = Order.query.all()
    total = calculate_total(orders)
    return render_template("cart.html", orders=orders, total=total)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/order")
def order():
    menu = Product.query.all()
    return render_template("order.html", menu=menu)


from flask import jsonify

@app.route("/order", methods=["POST"])
def create_order():
    try:
        data = json.loads(request.get_json())
        if not data:
            return jsonify({"error": "No data provided"}), 400
    except:
        return jsonify({"error": "Invalid JSON"}), 400

    for key in ("name", "address", "products"):
        if key not in data:
            return jsonify({"error": f"The JSON is missing: {key}"}), 400
        
    if not data['products']:
        return jsonify({"error": "No products provided"}), 400
    
    if not data['name']:
        return jsonify({"error": "No name provided"}), 400
    
    if not data['address']:
        return jsonify({"error": "No address provided"}), 400
    
    products = []
    for category in data['products']:
        for product in data['products'][category]:
            current_product = db.session.query(Product).filter_by(name=product['name']).first()
            if not current_product:
                return jsonify({"error": f"The product {product['name']} does not exist"}), 404
            products.append({'product':current_product, 'count':product['count']})

    order = Order(
        name=data['name'],
        address=data['address'],
    )

    for product in products:
        association = ProductsOrder(
            product=product['product'],
            order=order,
            quantity=product["count"],
        )
        db.session.add(association)
    db.session.add(order)
    db.session.commit()

    return jsonify({"location": url_for("cart")})


@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


@app.route("/feedback", methods=["POST"])
def create_feedback():
    message = request.get_json()["message"]
    feedback = Feedback(message=message)

    db.session.add(feedback)
    db.session.commit()

    return redirect(url_for("feedback"))


if __name__ == "__main__":
    app.run()
