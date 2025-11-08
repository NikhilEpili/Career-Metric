from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_user() -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User",
        },
    )
    assert response.status_code in [201, 400]  # 400 if user already exists


def test_login_user() -> None:
    # First register
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "logintest@example.com",
            "password": "TestPassword123!",
        },
    )

    # Then login
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "logintest@example.com",
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials() -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "WrongPassword",
        },
    )
    assert response.status_code == 400

