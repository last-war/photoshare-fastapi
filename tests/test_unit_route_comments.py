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


def test_post_comment(client, token):
    response = client.post("/api/comments/1", json={"comment_text": "Test text for new comment"}, 
                           headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    body_data = response.json()
    assert body_data == {
        "id": 1,
        "user_id": 1,
        "image_id": 1,
        "comment_text": "Test text for new comment",
        "created_at": f"{body_data['created_at']}",
        "updated_at": None,
    }


def test_show_user_comments(client, token):
    response = client.get("/api/comments/user/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["id"] == 1


def test_show_comments(client, token):
    response = client.get("api/comments/image/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["id"] == 1


def test_update_comment(client, token):
    response = client.put(
        "api/comments/1", json={"comment_text": "NEW Test text for comment"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    body_data = response.json()
    assert body_data == {
        "id": 1,
        "user_id": 1,
        "image_id": 1,
        "comment_text": "NEW Test text for comment",
        "created_at": f"{body_data['created_at']}",
        "updated_at": f"{body_data['updated_at']}",
    }


def test_remove_comment(client, token):
    response = client.delete("/api/comments/100", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response = client.delete("/api/comments/{image_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
