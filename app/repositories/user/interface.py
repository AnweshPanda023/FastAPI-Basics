from typing import Protocol

from sqlalchemy import Sequence

from app.models.user import User


class IUserRepository(Protocol):

    def get_by_email(self, email: str) -> User | None: ...

    def create(self, user: User) -> User: ...

    def get_by_id(self, id: int) -> User | None: ...

    def update(self, user: User) -> User: ...

    def get_all(
        self,
        offset: int,
        limit: int,
        search: str | None = None,
        role: str | None = None,
        is_active: bool | None = None,
    ) -> list[User]: ...

    def count_all(
        self,
        search: str | None = None,
        role: str | None = None,
        is_active: bool | None = None,
    ) -> int: ...
