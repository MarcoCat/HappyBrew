import pytest

from app import app, db


# TODO: fix deletes all data from the database
@pytest.fixture(scope="module")
def test_client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

    with app.app_context():
        db.drop_all()
