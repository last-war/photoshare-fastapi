import unittest
from unittest.mock import MagicMock


from sqlalchemy.orm import Session

from src.database.models import Rating, User, Image
from src.repository.ratings import (
    create_rate,
    delete_rate,
    calculate_rating,
    show_images_by_rating
)


class TestRatings(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.test_user = User(
            id=1,
            login='SuperUser',
            email='user@super.com',
            password_checksum='superpwd',
            is_active=True,
        )

    def tearDown(self):
        self.session = None
        self.test_user = None

    # test create_rate function from src/repository/ratings.py with different inputs
    async def test_create_rate_own_image(self):
        # test if it is not possible to rate own image
        self.session.query().filter().order_by().first.return_value = Image(
            id=1,
            image_url='test_image',
            description='test_path',
            user_id=1,
        )
        with self.assertRaises(Exception):
            await create_rate(image_id=1, rate=5, db=self.session, user=self.test_user)

    async def test_create_rate_twice(self):
        # test if it is not possible to rate twice
        self.session.query().filter().order_by().first.return_value = Rating(
            id=1,
            image_id=1,
            rate=5,
            user_id=1,
        )
        with self.assertRaises(Exception):
            await create_rate(image_id=1, rate=5, db=self.session, user=self.test_user)

    async def test_create_rate_image_not_exists(self):
        # test if it is not possible to rate an image that does not exist
        self.session.query().filter().order_by().first.return_value = None
        with self.assertRaises(Exception):
            await create_rate(image_id=1, rate=5, db=self.session, user=self.test_user)

    async def test_create_rate(self):
        # test if it is possible to rate an image
        self.session.query().filter().order_by().first.return_value = None
        self.session.query().filter().order_by().first.return_value = Image(
            id=2,
            image_url='test_image',
            description='test_path',
            user_id=2,
        )
        result = await create_rate(image_id=2, rate=5, db=self.session, user=self.test_user)
        self.assertIsInstance(result, Rating)

    async def test_delete_rate(self):
        # test if it is possible to delete a rate
        self.session.query().filter().order_by().first.return_value = Rating(
            id=1,
            image_id=1,
            rate=5,
            user_id=1,
        )
        result = await delete_rate(rate_id=1, db=self.session, user=self.test_user)
        self.assertIsNone(result)

    async def test_calculate_rating(self):
        # test if it is possible to calculate rate
        self.session.query().filter().order_by().first.return_value = Rating(
            id=1,
            image_id=1,
            rate=5,
            user_id=1,
        )
        result = await calculate_rating(image_id=1, db=self.session, user=self.test_user)
        self.assertEqual(result, 5)

    async def test_show_images_by_rating(self):
        # test if it is possible to show images by rating
        self.session.query().filter().order_by().first.return_value = Rating(
            id=1,
            image_id=1,
            rate=5,
            user_id=1,
        )
        result = await show_images_by_rating(True, db=self.session, user=self.test_user)
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()