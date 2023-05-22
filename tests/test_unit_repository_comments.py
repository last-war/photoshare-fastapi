import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Comment, User
from src.schemas.comments import CommentBase, CommentResponse
from src.repository.comments import (
    get_all_user_comments,
    get_comments_by_image_id,
    create_comment,
    delete_comment,
    edit_comment,
)


class TestComments(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.test_user = User(id=1,
                              login='SomeLogin',
                              email='someemail@gmail.com',
                              role=1,
                              user_pic_url='https://www.gravatar.com/avatar/94d093eda664addd6e450d7e9881bcad?s=32&d'
                                           '=identicon&r=PG',
                              name='Somename',
                              is_active=True,
                              password_checksum='secret')
        
    async def test_get_all_user_comments(self):
        comments = [Comment(), Comment(), Comment()]
        self.session.query().filter().offset().limit().all.return_value = comments
        result = await get_all_user_comments(skip=0, limit=10, user_id=self.test_user.id, db=self.session)
        self.assertEqual(result, comments)


    async def test_get_comments_by_image_id(self):
        comments = [Comment(), Comment(), Comment()]
        self.session.query().filter().offset().limit().all.return_value = comments
        result = await get_comments_by_image_id(skip=0, limit=10, image_id=1, db=self.session)
        self.assertEqual(result, comments)


    async def test_create_comment(self):
        image_id = 1
        body = CommentBase(comment_text='test_comment')
        result = await create_comment(image_id=image_id, body=body, db=self.session, user=self.test_user)
        self.assertEqual(result.comment_text, body.comment_text)
        self.assertEqual(result.image_id, image_id)
        self.assertTrue(hasattr(result, "id"))


    async def test_delete_comment_found(self):
        comment = Comment()
        self.session.query().filter().first.return_value = comment
        result = await delete_comment(comment_id=1, db=self.session, user=self.test_user)
        self.assertEqual(result, comment)


    async def test_delete_comment_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await delete_comment(comment_id=1, db=self.session, user=self.test_user)
        self.assertIsNone(result)
    

    async def test_edit_comment_found(self):
        body = CommentBase(comment_text='test_comment')
        comment = Comment()
        self.session.query().filter().first.return_value = comment
        self.session.commit.return_value = None
        result = await edit_comment(comment_id=1, body=body, db=self.session, user=self.test_user)
        self.assertEqual(result, comment)


    async def test_edit_comment_not_found(self):
        body = CommentBase(comment_text='test_comment')
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await edit_comment(comment_id=1, body=body, db=self.session, user=self.test_user)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()