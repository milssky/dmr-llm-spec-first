from django.test import Client


def test_pet_status_route_smoke() -> None:
    response = Client().get("/pet/findByStatus", {"status": "available"})
    assert response.status_code == 200
    assert response.json() == []


def test_store_inventory_route_smoke() -> None:
    response = Client().get("/store/inventory")
    assert response.status_code == 200
    assert response.json() == {}


def test_user_login_route_smoke() -> None:
    response = Client().get("/user/login", {"username": "demo", "password": "pw"})
    assert response.status_code == 200
    assert "X-Rate-Limit" in response.headers
    assert "X-Expires-After" in response.headers
