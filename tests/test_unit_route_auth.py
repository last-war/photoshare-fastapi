from _pytest.fixtures import fixture
from fastapi import status

from src.database.models import User, UserRole


@fixture(scope='function')
def token(client, user, session):
    response = client.post("/api/auth/signup",
                           json={"login": "deadpool",
                                 "email": "deadpool@example.com",
                                 "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.role = UserRole.Admin
    session.commit()
    response = client.post("/api/auth/login",
                           data={"username": "deadpool@example.com",
                                 "password": "123456789"},
                           headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = response.json()
    return data["access_token"]


def test_signup(client, user, session):
    response = client.post("api/auth/signup", json=user)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("api/auth/signup", json=user)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_login(client):
    response = client.post("/api/auth/login",
                           data={"username": "deadpool@example.com",
                                 "password": "123456789"},
                           headers={'Content-Type': 'application/x-www-form-urlencoded'})

    assert response.status_code == status.HTTP_200_OK
    response = client.post("/api/auth/login",
                           data={"username": "deadpool@example.com",
                                 "password": "444"},
                           headers={'Content-Type': 'application/x-www-form-urlencoded'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_wrong_user_data(client):
    response = client.post("/api/auth/login",
                           data={"username": "not_found@example.com",
                                 "password": "123456789"},
                           headers={'Content-Type': 'application/x-www-form-urlencoded'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout(client, token):
    response = client.post("api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK


def test_refresh_token(client, token):
    response = client.get("api/auth/refresh_token", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    response = client.get("api/auth/refresh_token")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
