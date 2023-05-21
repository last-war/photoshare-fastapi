from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer  # Bearer token
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    @classmethod
    def token_decode(cls, token: str) -> dict:
        """
            Try to decode the token

        Arguments:
            token (str): token to take decoded

        Returns:
            dict with results of decoded token
        """
        try:
            return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        except JWTError:
            raise cls.credentials_exception

    @classmethod
    async def create_access_token(cls, data: dict, expires_delta: Optional[float] = None) -> dict:
        """
        The create_access_token function creates a new access token for the user.
            The function takes in two arguments: data and expires_delta.
            Data is a dictionary that contains all of the information about the user,
            such as their username, email address, etc.
            Expires_delta is an optional argument that specifies how long you want your access token to be valid
            for (in seconds). If no value is specified then it defaults to 48 hours.

        Arguments:
            data (dict): A dictionary containing the user's id and username.
            expires_delta (Optional[float]): The number of seconds until the token expires, defaults to None.

        Returns:
            A token that is encoded with the data, current time, expiry time and scope
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(hours=48)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_access_token

    @classmethod
    async def create_refresh_token(cls, data: dict, expires_delta: Optional[float] = None):
        """
        The create_refresh_token function creates a refresh token for the user.

        Arguments:
            data (dict): A dictionary containing the user's id and username.
            expires_delta (Optional[float]): Set the expiration time of the refresh token

        Returns:
            An encoded refresh token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_refresh_token

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        The get_current_user function is a dependency that will be used in the
            protected endpoints. It takes a token as an argument and returns the user
            if it's valid, or raises an exception otherwise.

        Arguments:
            token (str): Get the token from the request header
            db (Session): SQLAlchemy session object for accessing the database

        Returns:
            A user object if the token is valid
        """

        payload = cls.token_decode(token)
        if payload.get("scope") == "access_token":
            email = payload.get("sub")
            if email is None:
                raise cls.credentials_exception
        else:
            raise cls.credentials_exception
        token_blacklisted = await repository_users.is_blacklisted_token(token, db)
        if token_blacklisted:
            raise cls.credentials_exception
        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise cls.credentials_exception
        return user

    @classmethod
    async def decode_refresh_token(cls, refresh_token: str):
        """
        The decode_refresh_token function is used to decode the refresh token.
        It takes a refresh_token as an argument and returns the email of the user if it's valid.
        If not, it raises an HTTPException with status code 401 (UNAUTHORIZED)
        and detail 'Could not validate credentials'.

        Arguments:
            refresh_token (str): Pass the refresh token to the function

        Returns:
            The email of the user that is associated with the refresh token
        """
        payload = cls.token_decode(refresh_token)
        if payload['scope'] == 'refresh_token':
            email = payload['sub']
            return email
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')

    @classmethod
    def create_email_token(cls, data: dict):
        """
        The create_email_token function takes a dictionary of data and returns a token.
        The token is encoded with the SECRET_KEY, which is stored in the .env file.
        The algorithm used to encode the token is also stored in the .env file.

        Arguments:
            data (dict): Pass in the data that will be encoded into the token

        Returns:
            A token that is encoded with the user's email and a secret key
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(hours=1)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "email_token"})
        token = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return token

    @classmethod
    def get_email_from_token(cls, token: str):
        """
        The get_email_from_token function takes a token as an argument and
        returns the email associated with that token.
        It does this by decoding the JWT using our SECRET_KEY and ALGORITHM,
        then checking to make sure that it has a scope of 'email_token'.
        If so, it returns the email address from the payload's sub field.
        If not, it raises an HTTPException with status code 401 (Unauthorized)
        and detail message &quot;Invalid scope for token&quot;.
        If there is any other error in decoding or validating the JWT, we raise another
        HTTPException with status code 422

        Arguments:
            token (str): Pass in the token that is sent to the user's email

        Returns:
            The email address associated with the token
        """
        payload = cls.token_decode(token)
        if payload['scope'] == 'email_token':
            email = payload['sub']
            return email
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')


auth_service = Auth()
