import datetime
from unittest.mock import patch

from pytest import fixture

from src.database.models import Tag, User, UserRole, Image
from src.schemas.tags import TagModel, TagResponse
from fastapi import status

from src.services.auth import auth_service


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
def image_user(client, user_user, session):
    response = client.post("/api/auth/signup", json={"login": "dead1pool", "email": "dead1pool@example.com",
                                                     "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user_user.get('email')).first()
    image = session.query(Image).filter(Image.id == 3).first()
    if image is None:
        image = Image(
            id=1,
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


def test_create_tags(client, session, token):
    """
    The test_create_tags function tests the POST /api/tag/{tags} endpoint.
    It does this by creating a new tag with the name &quot;test&quot; and then checking that it was created correctly.

    Args:
        client: Make requests to the api
        session: Query the database for tags
        token: Authenticate the user

    Returns:
        A 201 status code and a list of dictionaries containing the tag name

    """
    tags_string = "test"
    response = client.post("/api/tag/%23test", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_201_CREATED, response.text

    expected_response = [{"id": 1, "tag_name": tags_string}]
    assert response.json() == expected_response

    tag = session.query(Tag).first()
    assert tag is not None
    assert tag.tag_name == tags_string


def test_create_tags_not_authorization(client, session):
    token = "not_valid"
    response = client.post("/api/tag/%23test", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


def test_create_tags_not_valid_tags(client, session, token):
    response = client.post("/api/tag/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_images_by_tag(client, session, token):
    tag_name = "test"
    limit = 10
    offset = 0

    tag = session.query(Tag).filter(Tag.id == 1).first()

    image = session.query(Image).filter(Image.id == 1).first()

    date = datetime.datetime.now()

    if image is None:
        image = Image(
            id=1,
            image_url="https://res.cloudinary.com/dy9mhswnt/image/upload/c_fill,g_faces,h_500,r_max,w_500"
                      "/v1/photoshare/333db2aa2c097073b2e971767d76f543960ce141f4acf4671e82369de8526e9e",
            user_id=1,
            created_at=date,
            description="est_image_test_image_test_image_test_image",
            tags=[tag]
        )
        session.add(image)
        session.commit()
        session.refresh(image)

    response = client.get("/api/tag/image/test", headers={"Authorization": f"Bearer {token}"},
                          params={"limit": limit, "offset": offset})

    assert response.status_code == status.HTTP_200_OK, response.text

    expected_response = [
        {
            "id": 1,
            "image_url": "https://res.cloudinary.com/dy9mhswnt/image/upload/c_fill,g_faces,h_500,r_max,w_500"
                         "/v1/photoshare/333db2aa2c097073b2e971767d76f543960ce141f4acf4671e82369de8526e9e",
            "user_id": 1,
            "created_at": date,
            "updated_at": date,
            "description": "est_image_test_image_test_image_test_image",
            "tags": [
                {
                    "id": 1,
                    "tag_name": "test"
                }
            ]
        }
    ]

    assert response.json()[0]["id"] == expected_response[0]["id"]
    assert response.json()[0]["image_url"] == expected_response[0]["image_url"]
    assert response.json()[0]["user_id"] == expected_response[0]["user_id"]
    assert response.json()[0]["description"] == expected_response[0]["description"]
    assert response.json()[0]["tags"][0]["id"] == expected_response[0]["tags"][0]["id"]
    assert response.json()[0]["tags"][0]["tag_name"] == expected_response[0]["tags"][0]["tag_name"]


def test_get_images_by_tag_not_found_images(client, session, token):
    limit = 10
    offset = 0

    response = client.get("/api/tag/image/testnotfound", headers={"Authorization": f"Bearer {token}"},
                          params={"limit": limit, "offset": offset})

    assert response.json() == []


def test_get_one_tag_found(client, session, token):
    tag = {
        "id": 1,
        "tag_name": "test"
    }
    response = client.get("/api/tag/test", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == tag


def test_get_one_tag_not_found(client, session, token):
    tag = None
    response = client.get("/api/tag/testnotfound", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


# def test_update_tag_found(client, session, token):
#     new_tag_name = "test_1"
#
#     response = client.put("/api/tag/test", headers={"Authorization": f"Bearer {token}"}, json={"tag_name": new_tag_name})
#
#     assert response.status_code == status.HTTP_200_OK, response.text


def test_delete_tag_found(client, session, token):
    response = client.delete("/api/tag/test", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    tag = session.query(Tag).filter(Tag.tag_name == "test").first()
    assert tag is None


def test_delete_tag_not_found(client, session, token):
    response = client.delete("/api/tag/test", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
