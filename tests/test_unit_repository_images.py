import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.database.models import User, Image
from src.schemas.images import ImageModel
from src.repository.images import (
    get_images,
    get_image,
    create,
    get_image_from_id,
    get_image_from_url,
    remove,
    change_description,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_images_found(self):
        expect_res = [Image(), ]
        self.session.query().filter().order_by().limit().offset().all.return_value = expect_res
        result = await get_images(limit=10, offset=0, user=self.user, db=self.session)
        self.assertEqual(result, expect_res)
        self.assertListEqual(result, expect_res)

    async def test_get_image_found(self):
        expect_res = Image()
        self.session.query().filter().order_by().first.return_value = expect_res
        result = await get_image(image_id=1, user=self.user, db=self.session)
        self.assertEqual(result, expect_res)

    async def test_get_image_not_found(self):
        self.session.query().filter().order_by().first.return_value = None
        result = await get_image(image_id=100, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_found(self):
        body = ImageModel(tags_text="last, python", description="test description test test")
        result = await create(body=body, image_url="image_url", user=self.user, db=self.session)
        self.assertEqual(result.description, body.description)
        self.assertListEqual(result.tags, [])
        self.assertTrue(hasattr(result, "id"))

    async def test_get_image_from_id_found(self):
        expect_res = Image()
        self.session.query().filter().first.return_value = expect_res
        result = await get_image_from_id(image_id=1, user=self.user, db=self.session)
        self.assertEqual(result, expect_res)

    async def test_get_image_from_id_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_image_from_id(image_id=100, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_image_from_url_found(self):
        expect_res = Image()
        self.session.query().filter().first.return_value = expect_res
        result = await get_image_from_url(image_url="photo/349856", user=self.user, db=self.session)
        self.assertEqual(result, expect_res)

    async def test_get_image_from_url_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_image_from_url(image_url="", user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_remove_found(self):
        expect_res = Image()
        self.session.query().filter().first.return_value = expect_res
        result = await remove(image_id=1, user=self.user, db=self.session)
        self.assertEqual(result, expect_res)

    async def test_remove_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove(image_id=100, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_change_description_found(self):
        expect_res = Image()
        body = ImageModel(tags_text="last, python", description="test description test test")
        self.session.query().filter().first.return_value = expect_res
        self.session.commit.return_value = None
        result = await change_description(body=body, image_id=1, user=self.user, db=self.session)
        self.assertEqual(result, expect_res)
        self.assertListEqual(result.tags, [])

    async def test_change_description_not_found(self):
        body = ImageModel(tags_text="last, python", description="test description test test")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await change_description(body=body, image_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()