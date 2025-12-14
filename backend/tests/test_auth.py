def test_user_registration_succeeds(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data


def test_user_is_persisted_and_password_is_hashed(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "realuser@example.com",
            "password": "securepassword"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "realuser@example.com"


def test_duplicate_email_registration_fails(client):
    response1 = client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )
    assert response1.status_code == 201

    response2 = client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )
    assert response2.status_code == 409
def test_login_with_valid_credentials_returns_token(client):
    # Register user first
    client.post(
        "/api/auth/register",
        json={
            "email": "loginuser@example.com",
            "password": "mypassword"
        }
    )

    # Attempt login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "loginuser@example.com",
            "password": "mypassword"
        }
    )

    # This MUST fail initially (RED)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
def test_protected_route_returns_current_user(client):
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "email": "me@example.com",
            "password": "mypassword"
        }
    )

    # Login user
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "me@example.com",
            "password": "mypassword"
        }
    )

    token = login_response.json()["access_token"]

    # Access protected route
    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # MUST fail initially (RED)
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
from datetime import timedelta

from app.core.security import create_access_token


def test_expired_token_is_rejected(client):
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "email": "expired@example.com",
            "password": "password123"
        }
    )

    # Create EXPIRED token manually
    expired_token = create_access_token(
        subject="expired@example.com",
        expires_delta=timedelta(minutes=-1),
    )

    # Access protected route
    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {expired_token}"
        }
    )

    # MUST fail (expired token)
    assert response.status_code == 401
def test_refresh_token_returns_new_access_token(client):
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "email": "refresh@example.com",
            "password": "mypassword"
        }
    )

    # Login user
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "refresh@example.com",
            "password": "mypassword"
        }
    )

    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]

    # Call refresh endpoint
    response = client.post(
        "/api/auth/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    # MUST FAIL INITIALLY (RED)
    assert response.status_code == 200
    assert "access_token" in response.json()
def test_refresh_token_rotation_revokes_old_token(client):
    # Register user
    client.post(
        "/api/auth/register",
        json={
            "email": "rotate@example.com",
            "password": "password123"
        }
    )

    # Login
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "rotate@example.com",
            "password": "password123"
        }
    )

    tokens = login_response.json()
    old_refresh_token = tokens["refresh_token"]

    # First refresh (valid)
    response1 = client.post(
        "/api/auth/refresh",
        json={"refresh_token": old_refresh_token}
    )

    assert response1.status_code == 200
    new_refresh_token = response1.json()["refresh_token"]

    # Second refresh using OLD token (must fail)
    response2 = client.post(
        "/api/auth/refresh",
        json={"refresh_token": old_refresh_token}
    )

    assert response2.status_code == 401

    # Refresh using NEW token (must succeed)
    response3 = client.post(
        "/api/auth/refresh",
        json={"refresh_token": new_refresh_token}
    )

    assert response3.status_code == 200





