def test_it_returns_status_code_200_on_products_route(client):
    response = client.get("/api/products")
    assert response.status_code == 200
