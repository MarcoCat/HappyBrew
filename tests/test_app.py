def test_routing(test_client):
    urls = ["/", "/about", "/instructions", "/login", "/signup"]
    for url in urls:
        response = test_client.get(url)
        assert response.status_code == 200
