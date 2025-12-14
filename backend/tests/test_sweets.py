import pytest
from app.models.user import User


def register_and_login(client, email, password):
    client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )
    login = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return login.json()["access_token"]


def promote_to_admin(db, email):
    user = db.query(User).filter(User.email == email).first()
    user.role = "admin"
    db.commit()


def test_admin_can_create_sweet(client, db):
    # register admin
    client.post(
        "/api/auth/register",
        json={"email": "admin@sweet.com", "password": "admin123"},
    )

    # promote to admin (test setup)
    promote_to_admin(db, "admin@sweet.com")

    # login
    token = register_and_login(client, "admin@sweet.com", "admin123")

    # create sweet
    response = client.post(
        "/api/sweets",
        json={
            "name": "Gulab Jamun",
            "category": "Indian",
            "price": 20.5,
            "quantity": 50,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Gulab Jamun"
    assert data["category"] == "Indian"
    assert data["price"] == 20.5
    assert data["quantity"] == 50


def test_authenticated_user_can_list_sweets(client):
    # register user
    token = register_and_login(
        client,
        email="user@sweet.com",
        password="user123",
    )

    # list sweets (empty initially)
    res = client.get(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    assert res.json() == []


def test_list_sweets_returns_created_items(client, db):
    # register admin
    client.post(
        "/api/auth/register",
        json={"email": "admin2@sweet.com", "password": "admin123"},
    )

    # promote to admin
    promote_to_admin(db, "admin2@sweet.com")

    # login admin
    token = register_and_login(client, "admin2@sweet.com", "admin123")

    # create sweet
    client.post(
        "/api/sweets",
        json={
            "name": "Rasgulla",
            "category": "Indian",
            "price": 15.0,
            "quantity": 30,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # list sweets
    res = client.get(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["name"] == "Rasgulla"
    assert data[0]["category"] == "Indian"

