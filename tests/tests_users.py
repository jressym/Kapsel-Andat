from fastapi.testclient import TestClient
from main2 import app

client = TestClient(app)


def test_create_user():
    response = client.post("/users", json={
        "username": "tester01",
        "email": "tester01@example.com",
        "password": "Abc123!@",
        "role": "staff"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "tester01"


def test_read_users_admin():
    response = client.get("/users?role=admin")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_users_staff():
    response = client.get("/users?role=staff&username=tester01")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["username"] == "tester01"


def test_update_user_as_admin():
    response = client.put("/users/1?role=admin", json={
        "email": "newmail@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newmail@example.com"


def test_delete_user_as_admin():
    response = client.delete("/users/1?role=admin")
    assert response.status_code == 204
