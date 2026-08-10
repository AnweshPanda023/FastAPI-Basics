from typing import Protocol

from app.models.enums import UserRole
from app.models.user import User


class IUserRepository(Protocol):

    def get_by_email(self, email: str) -> User | None: ...

    def create(self, user: User) -> User: ...

    def get_by_id(self, id: int) -> User | None: ...

    def update_role(
        self,
        user: User,
        role: UserRole,
    ) -> User: ...
