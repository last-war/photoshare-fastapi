from typing import List

from fastapi import Depends, HTTPException, status, Request

from src.database.models import User, UserRole
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: List[UserRole]):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and takes in any arguments that are required to do so.
        In this case, we're taking in a list of allowed roles.

        Arguments:
            allowed_roles (List[UserRole]): Create a list of roles that are allowed to use the command

        Returns:
            None
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, current_user: User = Depends(auth_service.get_current_user)):
        """
        The __call__ function is the function that will be called when a user tries to access an endpoint.
        It takes in two arguments: request and current_user. The request argument is the Request object, which contains
        information about the HTTP request made by a client (e.g., headers, body).
        The current_user argument is provided by Depends(auth_service.get_current_user), which means it will call
        auth_service's getCurrentUser() function and pass its return value as an argument to __call__.

        Arguments:
            current_user (User): Get the current user from the auth_service
            request (Request): Get the request object

        Returns:
            The decorated function
        """
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Operation forbidden')