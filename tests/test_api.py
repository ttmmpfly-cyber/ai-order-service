def test_health(client):
    response =client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }

def test_get_existing_order(client):
    response = client.get(
        "/orders/A1001"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["order_id"] == "A1001"
    assert data["status"] == "shipped"
    assert data["paid"] is True

def test_get_nonexistent_order(client):
    response = client.get(
        "/orders/A9999"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Order not found"
    }