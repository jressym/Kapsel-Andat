from fastapi.testclient import TestClient
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_create_item():
    payload = {
        "id": 1,
        "name": "ITEM TEST",
        "description": "For unit test",
        "price": 99.9
    }

    response = client.post("/items", json=payload)
    assert response.status_code == 200
    assert response.json() == payload

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "ITEM TEST"

def test_update_item():
    payload = {
        "id": 1,
        "name": "ITEM TEST UPDATED",
        "description": "Updated description",
        "price": 150.0
    }
    response = client.put("/items/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ITEM TEST UPDATED"
    assert data["price"] == 150.0

def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data ["message"] == "Item 1 deleted"

    response = client.get("/items/1")
    assert response.status_code == 404 or "error" in response.json()