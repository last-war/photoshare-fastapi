from unittest.mock import MagicMock, patch
import io

from pytest import fixture, mark

from src.database.models import User, UserRole
from fastapi import status

from src.repository.users import update_token


@fixture(scope='function')
def token(client, user, session):
    response = client.post("/api/auth/signup", json={"login": "deadpool", "email": "deadpool@example.com",
                                                     "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.role = UserRole.Admin
    session.commit()
    response = client.post("/api/auth/login", data={
                            "username": "deadpool@example.com",
                            "password": "123456789"}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = response.json()
    return data["access_token"]


@fixture(scope='function')
def token_moder(client, user, session):
    response = client.post("/api/auth/signup", json={"login": "deadpool", "email": "deadpool@example.com",
                                                     "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.role = UserRole.Moderator
    session.commit()
    response = client.post("/api/auth/login", data={
                            "username": "deadpool@example.com",
                            "password": "123456789"}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = response.json()
    return data["access_token"]


@fixture(scope='function')
def token_user(client, user, session):
    response = client.post("/api/auth/signup", json={"login": "deadpool", "email": "deadpool@example.com",
                                                     "password_checksum": "123456789"})
    response = client.post("/api/auth/login", data={
                            "username": "deadpool@example.com",
                            "password": "123456789"}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = response.json()
    return data["access_token"]


def test_create_transformation_image(client, token):
    response = client.post("/api/images/transformation")
    assert response.status_code == status.HTTP_200_OK


def test_get_images_by_admin(client, token):
    response = client.get("/api/images/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK


def test_get_images_by_moder(client, token_moder):
    response = client.get("/api/images/", headers={"Authorization": f"Bearer {token_moder}"})
    assert response.status_code == status.HTTP_200_OK


def test_get_images_by_user(client, token_user):
    response = client.get("/api/images/", headers={"Authorization": f"Bearer {token_user}"})
    assert response.status_code == status.HTTP_200_OK


def test_get_image(client, token):
    response = client.get("/api/images/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/api/images/100", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_remove_image(client, token):
    response = client.delete("/api/images/{image_id}")
    assert response.status_code == status.HTTP_200_OK


def test_update_description_image(client, token):
    response = client.patch("/api/images/description/{image_id}")
    assert response.status_code == status.HTTP_200_OK


def test_create_image(client, token):
    image_url = 'https://res.cloudinary.com/dy9mhswnt/image/upload/c_fill,g_faces,h_500,r_max,w_500/v1/photoshare' \
                '/473db2aa2c097073b2e971767d76f543960ce141f4acf4671e82369de8526e9e'
    image_file = io.BytesIO(image_url.encode())
    response = client.post(
        "/api/images",
        data={"description": "test_image_test_image_test_image_test_image",
            "tags_text": "#python",
            },
        files={"image_file": image_file}
            ,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "multipart/form-data"},
    )

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["description"] == "test_image_test_image_test_image_test_image"
    assert data["id"] == 1
    assert "id" in data
