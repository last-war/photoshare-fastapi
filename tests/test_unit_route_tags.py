from pytest import fixture

from src.database.models import Tag, User, UserRole
from src.schemas.tags import TagModel, TagResponse
from fastapi import status


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


def test_create_tags(client, session, token):
    tags_string = "#test_tag"
    response = client.post(f"/api/tag/{tags_string}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_201_CREATED, response.text

    expected_response = [TagResponse(id=1, tag_name=tags_string)]
    assert response.json() == expected_response

    tag = session.query(Tag).first()
    assert tag is not None
    assert tag.tag_name == tags_string
