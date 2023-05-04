from app import app, db
from models import Product

products = [
    ("Mango smoothie", 6.50, "Seasonal only", "Special seasonal fruit", 100),
    (
        "Grape smoothie",
        6.50,
        "Seasonal only",
        "Special seasonal fruit with bubble",
        100,
    ),
    (
        "Watermelon and Coconut Slush",
        7.50,
        "Seasonal only",
        "Special seasonal fruit with Sago",
        100,
    ),
    ("Milk Tea", 4.50, "Milk Tea Series", "Just a normal milk tea", 100),
    (
        "Bubble Tea",
        5.00,
        "Milk Tea Series",
        "Milk tea but it has pearls this time",
        100,
    ),
    (
        "Black Tea Latte",
        4.50,
        "Milk Tea Series",
        "A delicious milk tea with more black tea base",
        100,
    ),
    (
        "Bubble Tea Latte",
        4.50,
        "Milk Tea Series",
        "A creamy milk tea with chewy pearls",
        100,
    ),
    ("Green Tea", 4.00, "Tea", "Just a normal green tea", 100),
]


with app.app_context():
    for product in products:
        obj = Product(
            name=product[0],
            price=product[1],
            category=product[2],
            description=product[3],
            quantity=product[4],
        )
        db.session.add(obj)
    db.session.commit()
    print("Successfully created all products.")
