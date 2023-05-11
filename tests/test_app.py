from models import User


def test_routing(test_client):
    urls = ["/", "/about", "/instructions", "/login", "/signup"]
    for url in urls:
        response = test_client.get(url)
        assert response.status_code == 200


def test_signup_successful(test_client):
    new_user = {
        "username": "test1",
        "password": "test1234",
        "confirm_password": "test1234",
    }
    response = test_client.post("/signup", data=new_user)
    assert response.status_code == 302
    assert User.query.filter_by(username=new_user["username"]).first() is not None


def test_signup_password_mismatch(test_client):
    new_user = {
        "username": "test2",
        "password": "test1234",
        "confirm_password": "test12345",
    }
    response = test_client.post("/signup", data=new_user)
    assert response.status_code == 200
    assert "Passwords do not match" in response.data.decode("utf-8")


def test_signup_username_taken(test_client):
    new_user = {
        "username": "test3",
        "password": "test1234",
        "confirm_password": "test1234",
    }
    response = test_client.post("/signup", data=new_user)
    assert response.status_code == 302
    assert User.query.filter_by(username=new_user["username"]).first() is not None
    response = test_client.post("/signup", data=new_user)
    assert response.status_code == 200
    assert "Username already taken" in response.data.decode("utf-8")
