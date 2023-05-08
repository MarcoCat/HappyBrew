import csv

from app import app, db
from models import Product

with app.app_context():
    db.create_all()
    print("Create all tables successfully.")

    with open("products.csv", newline="") as csvfile:
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
