import io
from PIL import Image as PILImage
from pytest import fixture

from src.database.models import User, UserRole, Image, Rating
from fastapi import status, UploadFile
import datetime


@fixture(scope='module')
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


@fixture(scope='module')
def token_moder(client, user_moder, session):
    response = client.post("/api/auth/signup", json={"login": "dead2pool", "email": "dead2pool@example.com",
                                                     "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user_moder.get('email')).first()
    current_user.role = UserRole.Moderator
    session.commit()
    response = client.post("/api/auth/login", data={
                            "username": "dead2pool@example.com",
                            "password": "123456789"}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = response.json()
    return data["access_token"]


@fixture(scope='module')
def token_user(client, user_user, session):
    response = client.post("/api/auth/signup", json={"login": "dead1pool", "email": "dead1pool@example.com",
                                                     "password_checksum": "123456789"})
    response = client.post("/api/auth/login", data={
                            "username": "dead1pool@example.com",
                            "password": "123456789"}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    data = response.json()
    return data["access_token"]


@fixture(scope='module')
def image(client, user, session):
    response = client.post("/api/auth/signup", json={"login": "deadpool", "email": "deadpool@example.com",
                                                     "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    image = session.query(Image).filter(Image.id == 1).first()
    if image is None:
        image = Image(
                    id=1,
                    image_url="https://res.cloudinary.com/dy9mhswnt/image/upload/c_fill,g_faces,h_500,r_max,w_500"
                                "/v1/photoshare/473db2aa2c097073b2e971767d76f543960ce141f4acf4671e82369de8526e9e",
                    user_id=current_user.id,
                    created_at=datetime.datetime.now(),
                    description="est_image_test_image_test_image_test_image"
        )
        session.add(image)
        session.commit()
        session.refresh(image)
    return image


@fixture(scope='module')
def image_moder(client, user_moder, session):
    response = client.post("/api/auth/signup", json={"login": "dead2pool", "email": "dead2pool@example.com",
                                                     "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user_moder.get('email')).first()
    image = session.query(Image).filter(Image.id == 2).first()
    if image is None:
        image = Image(
                    id=2,
                    image_url="https://res.cloudinary.com/dy9mhswnt/image/upload/c_fill,g_faces,h_500,r_max,w_500"
                                "/v1/photoshare/223db2aa2c097073b2e971767d76f543960ce141f4acf4671e82369de8526e9e",
                    user_id=current_user.id,
                    created_at=datetime.datetime.now(),
                    description="est_image_test_image_test_image_test_image"
        )
        session.add(image)
        session.commit()
        session.refresh(image)
    return image


@fixture(scope='module')
def image_user(client, user_user, session):
    response = client.post("/api/auth/signup", json={"login": "dead1pool", "email": "dead1pool@example.com",
                                                     "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user_user.get('email')).first()
    image = session.query(Image).filter(Image.id == 3).first()
    if image is None:
        image = Image(
                    id=3,
                    image_url="https://res.cloudinary.com/dy9mhswnt/image/upload/c_fill,g_faces,h_500,r_max,w_500"
                                "/v1/photoshare/333db2aa2c097073b2e971767d76f543960ce141f4acf4671e82369de8526e9e",
                    user_id=current_user.id,
                    created_at=datetime.datetime.now(),
                    description="est_image_test_image_test_image_test_image"
        )
        session.add(image)
        session.commit()
        session.refresh(image)
    return image


def test_show_images_by_rating(client, token, image, session):
    response = client.get("/api/ratings/images", headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data[0].get('id') == image.id


def test_show_images_by_rating_moder(client, token_moder, image_moder, session):
    response = client.get("/api/ratings/images", headers={'Authorization': f'Bearer {token_moder}'})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data[0].get('id') == image_moder.id


# WORK IN PROGRESS
