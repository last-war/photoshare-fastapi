import unittest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from src.services.cloud_image import CloudImage
from src.repository import images as repository _images


from main import app


class TestCreateImage(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_image_success(self):
        response = self.client.post(
            "/images/",
            headers={"X-Token": "coneofsilence"},
            json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json() == {
    "id": 0,
    "image_url": "string",
    "user_id": 0,
    "created_at": "2023-05-19T19:48:22.217Z",
    "updated_at": "2023-05-19T19:48:22.217Z",
    "description": "string",
    "tags": [
            {
                "id": 0,
                "tag_name": "string"
            }
            ]
    })

    def test_your_route_success(self):
        # Make a request to your route
        response = self.client.get('/')

        # Assert the expected response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Welcome to the FAST API from team 6'})


if __name__ == '__main__':
    unittest.main()
