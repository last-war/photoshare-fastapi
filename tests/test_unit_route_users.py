from pytest import fixture

from src.database.models import User, UserRole
from fastapi import status


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


def test_read_users_me(client, token):
    response = client.get("api/users/me/",
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    response = client.get("api/users/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_read_user_profile_by_username(client, token, user):
    login = user['login']
    response = client.get(f"api/users/user/{login}/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    login = 'test_wrong_login'
    response = client.get(f"api/users/user/{login}/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user(client, token):
    response = client.put("api/users/update_user",
                          headers={"Authorization": f"Bearer {token}"},
                          json={
                              "id": 0,
                              "email": "string",
                              "updated_at": "2023-05-21T16:35:59.380Z",
                              "user_pic_url": "string",
                              "name": "string",
                              "password_checksum": "string"})
    assert response.status_code == status.HTTP_200_OK

    response = client.put("api/users/update_user")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
