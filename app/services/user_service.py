import math

from app.core.security import hash_password, verify_password
from app.db.unit_of_work import UnitOfWork
from app.exceptions.auth import (
    EmailAlreadyExistsException,
    InvalidCurrentPasswordException,
    UserNotFoundException,
    RoleNotFoundException,
)
from app.models.user import User
from app.repositories.refresh_token.interface import IRefreshTokenRepository
from app.repositories.role.interface import IRoleRepository
from app.repositories.user.interface import IUserRepository


class UserService:

    def __init__(
        self,
        user_repository: IUserRepository,
        unit_of_work: UnitOfWork,
        role_repository: IRoleRepository,
        refresh_token_repository: IRefreshTokenRepository,
    ):
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work
        self.role_repository = role_repository
        self.refresh_token_repository = refresh_token_repository

    def update_role(
        self,
        user_id: int,
        role: str,
    ) -> User:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException()

        role_name = role.strip().lower()

        new_role = self.role_repository.get_by_name(role_name)

        if new_role is None:
            raise RoleNotFoundException()

        user.role = new_role

        with self.unit_of_work:
            self.user_repository.update(user)

        return user

    def get_all_users(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        role: str | None = None,
        is_active: bool | None = None,
    ):
        offset = (page - 1) * page_size

        users = self.user_repository.get_all(
            offset=offset,
            limit=page_size,
            search=search,
            role=role,
            is_active=is_active,
        )

        total = self.user_repository.count_all(
            search=search,
            role=role,
            is_active=is_active,
        )

        total_pages = math.ceil(total / page_size)

        return {
            "items": users,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
        }

    def update_profile(
        self,
        user_id: int,
        email: str | None,
        full_name: str | None,
    ) -> User:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException()

        if email is not None:
            email = email.strip().lower()

            existing_user = self.user_repository.get_by_email(email)

            if existing_user is not None and existing_user.id != user.id:
                raise EmailAlreadyExistsException()

            user.email = email

        if full_name is not None:
            user.full_name = full_name.strip()

        with self.unit_of_work:
            self.user_repository.update(user)

        return user

    def change_password(
        self,
        user: User,
        current_password: str,
        new_password: str,
    ) -> None:

        if not verify_password(
            current_password,
            user.password_hash,
        ):
            raise InvalidCurrentPasswordException()

        if verify_password(
            new_password,
            user.password_hash,
        ):
            raise SamePasswordException()

        with self.unit_of_work:

            user.password_hash = hash_password(new_password)

            self.user_repository.update(user)

            self.refresh_token_repository.revoke_all_for_user(user.id)
