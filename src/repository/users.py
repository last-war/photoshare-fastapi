from datetime import datetime

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User, UserRole
from src.schemas import UserModel, UserResponse
from src.services.auth import auth_service
from src.services.roles import RoleAccess


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user with that email if it exists. If no such user exists,
    it returns None.

    :param email: str: Pass in the email of the user we want to find
    :param db: Session: Pass the database session to the function
    :return: A user object or none if the user is not found
    :doc-author: Trelent
    """
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.

    :param body: UserModel: Pass in the UserModel object that is created from the request body
    :param db: Session: Pass the database session to the function
    :return: A user object, which is the same as what we return from our get_user function
    :doc-author: Trelent
    """
    g = Gravatar(body.email)
    new_user = User(**body.dict(), user_pic_url=g.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, refresh_token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Pass the user object to the function
    :param refresh_token: str | None: Pass the refresh token to the update_token function
    :param db: Session: Pass the database session to the function
    :return: Nothing
    :doc-author: Trelent
    """
    user.refresh_token = refresh_token
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :param url: str: Pass in the url of the avatar that we want to update
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def update_user(body: UserResponse, user: User, db: Session) -> User | None:
    """
    Updates user profile.
    Logged-in user can update his information.

    :param body: A set of user attributes to update.
    :type body: UserBase
    :param user: Logged-in user.
    :type user: User.
    :param db: Database session.
    :type db: Session.
    :return: Updated user.
    :rtype: User or None
    """
    user = db.query(User).filter(User.id == user.id).first()
    if user:
        user.name = body.name
        user.email = body.email
        user.user_pic_url = body.user_pic_url
        user.password_checksum = auth_service.get_password_hash(body.password_checksum)
        user.updated_at = datetime.now()
        db.commit()
    return user


async def update_user_by_admin(body: UserResponse, user: User, db: Session) -> User | None:
    """
    Updates user profile.
    Logged-in admin can update any profile.

    :param body: A set of user attributes to update.
    :type body: UserUpdate
    :param user: User.
    :type user: User.
    :param db: Database session.
    :type db: Session.
    :return: Updated user.
    :rtype: User or None
    """
    user_to_update = db.query(User).filter(User.login == body.login).first()
    if user_to_update:
        if user.role == RoleAccess([UserRole.Admin]):
            user_to_update.login = body.login
            user_to_update.name = body.name
            user_to_update.email = body.email
            user_to_update.is_active = body.is_active
            user_to_update.role = body.role
            user_to_update.user_pic_url = body.user_pic_url
            user_to_update.password_checksum = auth_service.get_password_hash(body.password_checksum)
            user_to_update.updated_at = datetime.now()
            db.commit()
        return user_to_update
    return None


async def ban_user(user_id: int, db: Session) -> User | None:
    """
    Sets user status to inactive.

    :param user_id: A user id to be banned.
    :type user_id: int
    :param db: Database session.
    :type db: Session.
    :return: Banned user if found.
    :rtype: User or None
    """
    user_to_ban = db.query(User).filter(User.id == user_id).first()
    if user_to_ban:
        user_to_ban.is_active = False
        db.commit()
        return user_to_ban
    return None
