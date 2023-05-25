from datetime import datetime

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User, BlacklistToken
from src.schemas.users import UserModel, UserChangeRole, UserUpdate, UserUpdateAdmin, UserShow
from src.services.auth import auth_service


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    Function takes in an email and a database session,
    and returns the user with that email if it exists. If no such user exists,
    it returns None.

    Arguments:
        email (str): Pass in the email of the user we want to find
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        User | None: A user object or None if the user is not found
    """
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.

    Arguments:
        body (UserModel): Pass in the UserModel object that is created from the request body
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        User: A user object, which is the same as what we return from our get_user function
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

    Arguments:
        user (User): Pass the user object to the function
        refresh_token (str | None): Pass the refresh token to the update_token function
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        None
    """
    user.refresh_token = refresh_token
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    Arguments:
        email (str): Find the user in the database by this email
        url (str): Pass in the url of the avatar that we want to update
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        User: A user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def update_user(body: UserUpdate, user: User, db: Session) -> User | None:
    """
    Updates user profile.
    Logged-in user can update his information.

    Arguments:
        body (UserUpdate): A set of user attributes to update
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        User | None: A user object or None
    """
    user = db.query(User).filter(User.id == body.id).first()
    if user:
        user.name = body.name
        user.email = body.email
        user.user_pic_url = body.user_pic_url
        user.password_checksum = auth_service.pwd_context.hash(body.password_checksum)
        user.updated_at = datetime.now()
        db.commit()
    return user


async def update_user_by_admin(body: UserUpdateAdmin, user: User, db: Session) -> User | None:
    """
    Updates user profile.
    Logged-in admin can update any profile.

    Arguments:
        body (UserUpdateAdmin): A set of user attributes to update
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        User | None: A user object or None
    """
    user_to_update = db.query(User).filter(User.id == body.id).first()
    if user_to_update:

        user_to_update.login = body.login
        user_to_update.name = body.name
        user_to_update.email = body.email
        user_to_update.is_active = body.is_active
        user_to_update.role = body.role
        user_to_update.user_pic_url = body.user_pic_url
        user_to_update.password_checksum = auth_service.pwd_context.hash(body.password_checksum)
        user_to_update.updated_at = datetime.now()
        db.commit()
        return user_to_update
    return None


async def change_role(body: UserChangeRole, user: User, db: Session) -> User | None:
    """
    Logged-in admin can change role of any profile by ID.

    Arguments:
        body (UserChangeRole): A set of user new role
        user (User): the current user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        User | None: A user object or None
    """
    user_to_update = db.query(User).filter(User.id == body.id).first()
    if user_to_update:
        user_to_update.role = body.role
        user_to_update.updated_at = datetime.now()
        db.commit()
        return user_to_update
    return None


async def ban_user(user_id: int, db: Session) -> User | None:
    """
    Sets user status to inactive.

    Arguments:
        user_id (int): A set of user new role
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        User | None: A user object or None
    """
    user_to_ban = db.query(User).filter(User.id == user_id).first()
    if user_to_ban:
        user_to_ban.is_active = False
        db.commit()
        return user_to_ban
    return None


async def get_user_profile(login: str, db: Session) -> UserShow | None:
    """
    function returns a UserShow object containing the user's information.

    Arguments:
        login (str): Get the user profile of a specific user
        db (Session): SQLAlchemy session object for accessing the database

    Returns:
        User | None: A UserShow object or None
    """
    user = db.query(User).filter(User.login == login).first()
    if user:
        user_profile = UserShow(
            id=user.id,
            login=user.login,
            email=user.email,
            role=user.role,
            user_pic_url=user.user_pic_url,
            name=user.name,
            is_active=user.is_active,
        )
        return user_profile
    return None


async def add_to_blacklist(token: str, db: Session) -> None:
    """
    Function adds a token to the blacklist.

    Arguments:
        token (str): The JWT that is being blacklisted.
        db (Session): SQLAlchemy session object for accessing the database
    Returns:
        None
    """
    blacklist_token = BlacklistToken(token=token, added_on=datetime.now())
    db.add(blacklist_token)
    db.commit()
    db.refresh(blacklist_token)
    return None


async def is_blacklisted_token(token: str, db: Session) -> bool:
    """
    Function takes checks if a token is blacklisted.

    Arguments:
        token (str): token to be checked
        db (Session): SQLAlchemy session object for accessing the database
    Returns:
        bool
    """
    blacklist_token = db.query(BlacklistToken).filter(BlacklistToken.token == token).first()
    if blacklist_token:
        return True
    return False
