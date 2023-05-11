from models import User


def test_routing(test_client):
    urls = ["/", "/about", "/instructions", "/login", "/signup"]
    for url in urls:
        response = test_client.get(url)
        assert response.status_code == 200


def test_signup(test_client, new_user):
    # test that user can sign up
    response = test_client.post("/signup", data=new_user)
    assert response.status_code == 302  # redirect to login page
    assert User.query.filter_by(username=new_user["username"]).first() is not None
