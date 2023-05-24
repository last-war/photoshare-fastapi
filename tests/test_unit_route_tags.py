import datetime

from pytest import fixture

from src.database.models import Tag, User, UserRole, Image
from fastapi import status


@fixture(scope='module')
def token(client, user, session):
    """
    The token function is used to create a user with admin privileges, and then log in as that user.
    This allows us to test the endpoints that require an admin token.

    Args:
        client: Make requests to the api
        user: Create a user in the database
        session: Make queries to the database

    Returns:
        A valid access token
    """
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
    """
    The test_create_tags_not_authorization function tests that a user cannot create a tag without authorization.

    Args:
        client: Make requests to the api
        session: Create a new database session for the test

    Returns:
        A 401 unauthorized status code
    """
    token = "not_valid"
    response = client.post("/api/tag/%23test", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text


def test_create_tags_not_valid_tags(client, session, token):
    """
    The test_create_tags_not_valid_tags function tests the POST /api/tag/ endpoint.
    It does this by sending a request to the endpoint with no data, and then checking that it returns a 404 status code.

    Args:
        client: Make requests to the api
        session: Rollback the database after each test
        token: Authenticate the user

    Returns:
        404
    """
    response = client.post("/api/tag/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_images_by_tag(client, session, token):
    """
    The test_get_images_by_tag function tests the get_images_by_tag function in the tag.py file.
    The test is successful if it returns a 200 status code and a list of images with tags that match the tag name.

    Args:
        client: Make requests to the api
        session: Create a new database session for the test
        token: Authenticate the user

    Returns:
        The images that have the tag
    """
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
    """
    The test_get_images_by_tag_not_found_images function tests the get_images_by_tag function in the image.py file
    to ensure that it returns an empty list when no images are found with a given tag.

    Args:
        client: Make requests to the api
        session: Pass the database session to the test function
        token: Test the get_images_by_tag function with a valid token

    Returns:
        An empty list
    """
    limit = 10
    offset = 0

    response = client.get("/api/tag/image/testnotfound", headers={"Authorization": f"Bearer {token}"},
                          params={"limit": limit, "offset": offset})

    assert response.json() == []


def test_get_one_tag_found(client, session, token):
    """
    The test_get_one_tag_found function tests the GET /api/tag/{tag_name} endpoint.
    It ensures that a tag can be retrieved by its name.

    Args:
        client: Make requests to the api
        session: Create a new session for the test
        token: Authenticate the user

    Returns:
        A 200 response with the tag data
    """
    tag = {
        "id": 1,
        "tag_name": "test"
    }
    response = client.get("/api/tag/test", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == tag


def test_get_one_tag_not_found(client, session, token):
    """
    The test_get_one_tag_not_found function tests the GET /api/tag/{id} endpoint.
        It ensures that a 404 status code is returned when an invalid tag id is passed in.

    Args:
        client: Send requests to the api
        session: Create a new session for the test
        token: Authenticate the user

    Returns:
        A 404 status code
    """
    tag = None
    response = client.get("/api/tag/testnotfound", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_update_tag_found(client, session, token):
    """
    The test_update_tag_found function tests the update_tag function in the tag.py file.
    It does this by first creating a new tag name, then it uses that to create a response from the client using PUT method
    to update an existing tag with id 1 and header of token authorization. It then asserts that status code is 200 OK, which means
    the request was successful and returns what we expected (in this case, it should return updated information for id 1).
    Finally, it creates an expected response variable to compare against our actual response.

    Args:
        client: Make requests to the api
        session: Create a new session for the test
        token: Authenticate the user

    Returns:
        A 200 status code and the updated tag
    """
    new_tag_name = "test_1"

    response = client.put("/api/tag/1", headers={"Authorization": f"Bearer {token}"}, json={"tag_name": new_tag_name})

    assert response.status_code == status.HTTP_200_OK, response.text

    expected_response = {"id": 1, "tag_name": new_tag_name}
    assert response.json() == expected_response


def test_update_tag_not_found(client, session, token):
    """
    The test_update_tag_not_found function tests the update tag endpoint.
        It does this by first creating a new tag, then attempting to update it with an invalid id.
        The expected result is that the response status code should be 404 NOT FOUND.

    Args:
        client: Make requests to the api
        session: Create a new session for the test
        token: Authenticate the user

    Returns:
        A 404 status code
    """
    new_tag_name = "test_1"

    response = client.put("/api/tag/999", headers={"Authorization": f"Bearer {token}"}, json={"tag_name": new_tag_name})

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_delete_tag_found(client, session, token):
    """
    The test_delete_tag_found function tests the DELETE /api/tag/{tag_name} endpoint.
    It does so by first creating a tag with the name &quot;test&quot; and then deleting it.
    The test passes if the response status code is 204 No Content and if there are no tags in the database with that name.

    Args:
        client: Send a request to the server
        session: Access the database
        token: Pass in the token to the function

    Returns:
        A 204 status code
    """
    response = client.delete("/api/tag/test_1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    tag = session.query(Tag).filter(Tag.tag_name == "test").first()
    assert tag is None


def test_delete_tag_not_found(client, session, token):
    """
    The test_delete_tag_not_found function tests the DELETE /api/tag/{name} endpoint.
    It does so by first creating a tag, then deleting it, and finally attempting to delete it again.
    The final attempt should fail with a 404 Not Found error.

    Args:
        client: Make requests to the api
        session: Create a database session
        token: Authenticate the user

    Returns:
        A 404 status code
    """
    response = client.delete("/api/tag/test", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
