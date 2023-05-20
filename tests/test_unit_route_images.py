from unittest.mock import MagicMock, patch

from pytest import fixture, mark

from src.database.models import User, UserRole
from fastapi import status

from src.services.auth import Auth
from src.repository.users import update_token


@fixture(scope='function')
def token(client, user, session):
    response = client.post("/api/auth/signup", json={"login": "deadpool", "email": "deadpool@example.com",
                                                     "password_checksum": "123456789"})
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.role = UserRole.Admin
    session.commit()
    print(response.json())
    response = client.post("/api/auth/login", json={
                            "grant_type": "",
                            "username": "deadpool@example.com",
                            "password": "123456789",
                            "scope": "",
                            "client_id": "",
                            "client_secret": ""}, content='application/x-www-form-urlencoded', )
    print(response.json())
    data = response.json()
    return data["access_token"]

def test_create_image(client, token):
    image_url = 'https://res.cloudinary.com/dy9mhswnt/image/upload/c_fill,g_faces,h_500,r_max,w_500/v1/photoshare' \
                '/473db2aa2c097073b2e971767d76f543960ce141f4acf4671e82369de8526e9e'
    response = client.post(
        "/api/images",
        json={"description": "test_image_test_image_test_image_test_image",
              "tags_text": "#python",
              "image_url": image_url, },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["description"] == "test_image_test_image_test_image_test_image"
    assert data["id"] == 1
    assert "id" in data
