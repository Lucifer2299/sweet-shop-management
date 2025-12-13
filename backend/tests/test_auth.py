from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_user_registration_fails_initially():
    """
    RED TEST:
    Endpoint does not exist yet.
    This test MUST fail.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201

