from pytest import fixture

from src.database.models import User, UserRole, Image, Rating
from fastapi import status
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
            user_id=5,
            created_at=datetime.datetime.now(),
            description="est_image_test_image_test_image_test_image",

        )
        session.add(image)
        session.commit()
        session.refresh(image)
    return image


@fixture(scope='module')
def rating(client, user, session):
    response = client.post("/api/auth/signup", json={"login": "deadpool", "email": "deadpool@example.com",
                                                     "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    rating = session.query(Image).filter(Rating.id == 1).first()
    if rating is None:
        rating = Rating(
            id=1,
            rate=5,
            user_id=current_user.id,
            image_id=1,
        )
        session.add(rating)
        session.commit()
        session.refresh(rating)
    return rating


def test_show_images_by_rating(client, token, image, session):
    response = client.get("/api/rating/show_images_by_rating?to_decrease=true",
                          headers={'Authorization': f'Bearer {token}'}
                          )
    assert response.status_code == status.HTTP_200_OK


def test_create_rate(client, token, image, session):
    response = client.post("/api/rating/1/5",
                           headers={'Authorization': f'Bearer {token}'}
                           )
    assert response.status_code == status.HTTP_200_OK


def test_delete_rate(client, token, session, rating):
    response = client.delete("/api/rating/delete/1",
                             headers={'Authorization': f'Bearer {token}'}
                             )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_show_image_rating(client, token, image, session):
    response = client.get("/api/rating/show_image_rating/1",
                          headers={'Authorization': f'Bearer {token}'}
                          )
    assert response.status_code == status.HTTP_200_OK
