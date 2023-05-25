import unittest
from datetime import datetime
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.repository.users import create_user, update_token, update_avatar, update_user, change_role, ban_user, \
    get_user_profile, update_user_by_admin
from src.schemas.users import UserModel, UserUpdate, UserChangeRole, UserShow, UserUpdateAdmin


class TestUsersRepository(unittest.IsolatedAsyncioTestCase):
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

    async def test_create_user(self):
        body = UserModel(login=self.test_user.login,
                         email=self.test_user.email,
                         password_checksum=self.test_user.password_checksum)

        res = await create_user(body=body, db=self.session)

        self.assertTrue(hasattr(res, "id"))
        self.assertEqual(res.login, body.login)
        self.assertEqual(res.email, body.email)
        self.assertEqual(res.password_checksum, body.password_checksum)

    async def test_update_token(self):
        user = self.test_user
        token = None
        result = await update_token(user=user, refresh_token=token, db=self.session)
        self.assertIsNone(result)

    async def test_update_avatar(self):
        url = 'https://res.cloudinary.com/'
        result = await update_avatar(email=self.test_user.email, url=url, db=self.session)
        self.assertEqual(result.avatar, url)

    async def test_change_role(self):
        body = UserChangeRole(id=self.test_user.id,
                              role=2,
                              updated_at=datetime.now())
        res = await change_role(body=body, user=self.test_user, db=self.session)
        self.assertEqual(res.role, body.role)

    async def test_change_role_not_found(self):
        body = UserChangeRole(id=100, role=2, updated_at=datetime.now())
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None

        result = await change_role(body=body, user=self.test_user, db=self.session)
        self.assertIsNone(result)

    async def test_get_user_profile(self):
        user_profile = UserShow(
            id=self.test_user.id,
            login=self.test_user.login,
            email=self.test_user.email,
            role=self.test_user.role,
            user_pic_url=self.test_user.user_pic_url,
            name=self.test_user.name,
            is_active=self.test_user.is_active,
        )

        self.session.query().filter().first.return_value = self.test_user

        res = await get_user_profile(login=self.test_user.login, db=self.session)

        self.assertEqual(res, user_profile)

    async def test_ban_user(self):
        res = await ban_user(user_id=1, db=self.session)
        self.assertEqual(res.is_active, False)

    async def test_ban_user_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await ban_user(user_id=100, db=self.session)
        self.assertIsNone(result)

    async def test_update_user(self):
        body = UserUpdate(id=self.test_user.id,
                          login=self.test_user.login,
                          email=self.test_user.email,
                          role=self.test_user.role,
                          user_pic_url=self.test_user.user_pic_url,
                          name="test_update",
                          password_checksum=self.test_user.password_checksum,
                          is_active=self.test_user.is_active,
                          )

        self.session.query().filter().first.return_value = self.test_user
        res = await update_user(body=body, user=self.test_user, db=self.session)
        self.assertEqual(res.name, "test_update")

    async def test_update_user_not_found(self):
        body = UserUpdate(id=100, email=self.test_user.email, password_checksum=self.test_user.password_checksum)
        self.session.query().filter().first.return_value = None
        res = await update_user(body=body, user=self.test_user, db=self.session)
        self.assertIsNone(res)

    async def test_update_user_by_admin(self):
        body = UserUpdateAdmin(id=self.test_user.id,
                               login=self.test_user.login,
                               email=self.test_user.email,
                               role=self.test_user.role,
                               user_pic_url=self.test_user.user_pic_url,
                               name="test_update_admin",
                               password_checksum=self.test_user.password_checksum,
                               is_active=self.test_user.is_active,
                               )

        self.session.query().filter().first.return_value = self.test_user
        res = await update_user_by_admin(body=body, user=self.test_user, db=self.session)
        self.assertEqual(res.name, "test_update_admin")

    async def test_update_user_by_admin_not_found(self):
        body = UserUpdateAdmin(id=self.test_user.id,
                               login=self.test_user.login,
                               email=self.test_user.email,
                               role=self.test_user.role,
                               user_pic_url=self.test_user.user_pic_url,
                               name="test_update_admin",
                               password_checksum=self.test_user.password_checksum,
                               is_active=self.test_user.is_active,
                               )
        self.session.query().filter().first.return_value = None
        res = await update_user_by_admin(body=body, user=self.test_user, db=self.session)
        self.assertIsNone(res)


if __name__ == '__main__':
    unittest.main()
