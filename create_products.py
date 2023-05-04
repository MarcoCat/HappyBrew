from app import app, db
from models import Product

products = [
    {
        "name": "Mango Smoothie",
        "price": 6.50,
        "category": "Seasonal Only",
        "description": "Special seasonal fruit",
    },
    {
        "name": "Grape Smoothie",
        "price": 6.50,
        "category": "Seasonal Only",
        "description": "Special seasonal fruit with bubble",
    },
    {
        "name": "Watermelon and Coconut Slush",
        "price": 7.50,
        "category": "Seasonal Only",
        "description": "Special seasonal fruit with Sago",
    },
    {
        "name": "Milk Tea",
        "price": 4.50,
        "category": "Milk Tea Series",
        "description": "Just a normal milk tea",
    },
    {
        "name": "Bubble Tea",
        "price": 5.00,
        "category": "Milk Tea Series",
        "description": "Milk tea but it has pearls this time",
    },
    {
        "name": "Black Tea Latte",
        "price": 4.50,
        "category": "Milk Tea Series",
        "description": "A delicious milk tea with more black tea base",
    },
    {
        "name": "Bubble Tea Latte",
        "price": 4.50,
        "category": "Milk Tea Series",
        "description": "A creamy milk tea with chewy pearls",
    },
    {
        "name": "Green Tea",
        "price": 4.00,
        "category": "Tea",
        "description": "Just a normal green tea",
    },
]


with app.app_context():
    for product in products:
        obj = Product(**product)
        db.session.add(obj)
    db.session.commit()
    print("Successfully created all products.")
