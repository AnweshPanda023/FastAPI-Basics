from collections.abc import Callable

from fastapi import Depends

from app.api.dependencies import get_current_user
from app.exceptions.authorization import (
    InsufficientPermissionsException,
)
from app.models.enums import UserRole
from app.models.user import User


def require_role(required_role: UserRole) -> Callable:

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role != required_role:
            raise InsufficientPermissionsException()

        return current_user

    return role_checker
