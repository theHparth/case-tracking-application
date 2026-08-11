import pytest
from app import models
from app.auth import hash_password


@pytest.fixture
def admin_user():
    from tests.conftest import TestSessionLocal
    db = TestSessionLocal()
    user = models.User(username="admin_test", hashed_password=hash_password("adminpass"), role=models.UserRole.admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


@pytest.fixture
def regular_user():
    from tests.conftest import TestSessionLocal
    db = TestSessionLocal()
    user = models.User(username="user_test", hashed_password=hash_password("userpass"), role=models.UserRole.user)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_success(client, regular_user):
    response = client.post("/token", data={"username": "user_test", "password": "userpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client, regular_user):
    response = client.post("/token", data={"username": "user_test", "password": "wrong"})
    assert response.status_code == 401


def test_non_admin_cannot_create_user(client, regular_user):
    login = client.post("/token", data={"username": "user_test", "password": "userpass"})
    token = login.json()["access_token"]
    response = client.post(
        "/users",
        json={"username": "new_user", "password": "somepass1", "role": "user"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_admin_can_create_user(client, admin_user):
    login = client.post("/token", data={"username": "admin_test", "password": "adminpass"})
    token = login.json()["access_token"]
    response = client.post(
        "/users",
        json={"username": "new_user", "password": "somepass1", "role": "user"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["username"] == "new_user"


def test_case_ownership(client, regular_user, admin_user):
    login = client.post("/token", data={"username": "user_test", "password": "userpass"})
    token = login.json()["access_token"]

    create = client.post(
        "/cases",
        json={"title": "Test case", "description": "desc"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create.status_code == 201

    admin_login = client.post("/token", data={"username": "admin_test", "password": "adminpass"})
    admin_token = admin_login.json()["access_token"]

    admin_list = client.get("/cases", headers={"Authorization": f"Bearer {admin_token}"})
    assert len(admin_list.json()) == 1

    user_list = client.get("/cases", headers={"Authorization": f"Bearer {token}"})
    assert len(user_list.json()) == 1