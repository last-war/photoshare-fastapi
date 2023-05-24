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


@fixture(scope='function')
def token_second(client, user, session):
    response = client.post("/api/auth/signup",
                           json={"login": "TEST",
                                 "email": "testpool@example.com",
                                 "password_checksum": "testpassword"})
    current_user: User = session.query(User).filter(User.email == 'testpool@example.com').first()
    current_user.role = UserRole.Admin
    session.commit()
    response = client.post("/api/auth/login",
                           data={"username": "testpool@example.com",
                                 "password": "testpassword"},
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


def test_change_role(client, user, token):
    response = client.put("api/users/change_role",
                          json={
                              "id": 1000,
                              "role": 2,
                              },
                          headers={"Authorization": f"Bearer {token}"},)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.put("api/users/change_role",
                          json={
                              "id": 1,
                              "role": 2,
                              },
                          headers={"Authorization": f"Bearer {token}"},)
    assert response.status_code == status.HTTP_200_OK

    response = client.put("api/users/change_role")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_user(client, token):
    response = client.put("api/users/update_user",
                          json={
                              "id": 12121,
                              "email": "deadpool@example.com",
                              "updated_at": "2023-05-21T16:35:59.380Z",
                              "user_pic_url": "string",
                              "name": "string",
                              "password_checksum": "123456789"},
                          headers={"Authorization": f"Bearer {token}"},)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.put("api/users/update_user",
                          headers={"Authorization": f"Bearer {token}"},
                          json={
                              "id": 1,
                              "email": "deadpool@example.com",
                              "updated_at": "2023-05-21T16:35:59.380Z",
                              "user_pic_url": "str495y2074y5804ying",
                              "name": "string",
                              "password_checksum": "123456789"})
    assert response.status_code == status.HTTP_200_OK

    response = client.put("api/users/update_user")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_user_by_admin(client, token_second):
    response = client.put("api/users/update_user_by_admin",
                          json={"id": 100,
                                "login": "deadpool_2",
                                "name": "deadpool_2",
                                "email": "testpool@example.com",
                                "is_active": True,
                                "role": 1,
                                "user_pic_url": "",
                                "password_checksum": "testpasswod",
                                "updated_at": "2023-05-21T16:35:59.380Z",},
                          headers={"Authorization": f"Bearer {token_second}"},)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.put("api/users/update_user_by_admin",
                          json={"id": 1,
                                "login": "TEST_USER",
                                "name": "test3",
                                "email": "test______test@example.com",
                                "is_active": True,
                                "role": 1,
                                "user_pic_url": "",
                                "password_checksum": "testpasswod",
                                "updated_at": "2023-05-21T16:35:59.380Z",},
                          headers={"Authorization": f"Bearer {token_second}"},)
    assert response.status_code == status.HTTP_200_OK
    print(response.json())

    response = client.put("api/users/update_user_by_admin")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_ban_user(client, user, token):
    response = client.put(f"api/users/ban_user/?user_id=1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    response = client.put(f"api/users/ban_user/?user_id=100", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

