import math

from app.db.unit_of_work import UnitOfWork
from app.exceptions.auth import UserNotFoundException, RoleNotFoundException
from app.models.user import User
from app.repositories.role.interface import IRoleRepository
from app.repositories.user.interface import IUserRepository


class UserService:

    def __init__(
        self,
        user_repository: IUserRepository,
        unit_of_work: UnitOfWork,
        role_repository: IRoleRepository,
    ):
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work
        self.role_repository = role_repository

    def update_role(
        self,
        user_id: int,
        role: str,
    ) -> User:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException("User not found")

        role = role.strip().lower()

        new_role = self.role_repository.get_by_name(role)

        if new_role is None:
            raise RoleNotFoundException()

        user.role = new_role

        with self.unit_of_work:
            self.user_repository.update_role(user, user.role)

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
