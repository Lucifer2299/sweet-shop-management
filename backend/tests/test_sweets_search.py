from app.models.sweet import Sweet
from app.models.user import User


def create_admin_and_token(client, db):
    client.post(
        "/api/auth/register",
        json={"email": "admin@sweet.com", "password": "admin123"},
    )

    admin = db.query(User).filter(User.email == "admin@sweet.com").first()
    admin.role = "admin"
    db.commit()

    login = client.post(
        "/api/auth/login",
        json={"email": "admin@sweet.com", "password": "admin123"},
    )

    return login.json()["access_token"]


def seed_sweets(db):
    sweets = [
        Sweet(name="Gulab Jamun", category="Indian", price=20, quantity=10),
        Sweet(name="Rasgulla", category="Indian", price=15, quantity=20),
        Sweet(name="Brownie", category="Bakery", price=50, quantity=5),
    ]
    db.add_all(sweets)
    db.commit()


def test_search_by_name(client, db):
    token = create_admin_and_token(client, db)
    seed_sweets(db)

    res = client.get(
        "/api/sweets/search?name=jam",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["name"] == "Gulab Jamun"


def test_search_by_category(client, db):
    token = create_admin_and_token(client, db)
    seed_sweets(db)

    res = client.get(
        "/api/sweets/search?category=Indian",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    assert len(res.json()) == 2


def test_search_by_price_range(client, db):
    token = create_admin_and_token(client, db)
    seed_sweets(db)

    res = client.get(
        "/api/sweets/search?min_price=10&max_price=30",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2


def test_search_combined_filters(client, db):
    token = create_admin_and_token(client, db)
    seed_sweets(db)

    res = client.get(
        "/api/sweets/search?category=Indian&max_price=18",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["name"] == "Rasgulla"

