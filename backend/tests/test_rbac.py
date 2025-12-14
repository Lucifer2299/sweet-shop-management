from app.core.security import hash_password
from app.models.user import User
from app.db.session import get_db

def create_user(client, email, password, role):
    db = next(client.app.dependency_overrides[get_db]())

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            hashed_password=hash_password(password),
            role=role,
        )
        db.add(user)
        db.commit()

def setup_users(client):
    create_user(client, "admin@example.com", "password123", "admin")
    create_user(client, "staff@example.com", "password123", "staff")
    create_user(client, "customer@example.com", "password123", "customer")

def login_as(client, email, password):
    res = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return res.json()["access_token"]

def test_non_admin_cannot_list_users(client):
    setup_users(client)
    token = login_as(client, "staff@example.com", "password123")

    res = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403

def test_admin_can_list_users(client):
    setup_users(client)
    token = login_as(client, "admin@example.com", "password123")

    res = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200

def test_staff_cannot_change_user_role(client):
    setup_users(client)
    token = login_as(client, "staff@example.com", "password123")

    res = client.patch(
        "/api/users/customer@example.com/role",
        json={"role": "admin"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403

def test_admin_can_change_user_role(client):
    setup_users(client)
    token = login_as(client, "admin@example.com", "password123")

    res = client.patch(
        "/api/users/customer@example.com/role",
        json={"role": "staff"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200

