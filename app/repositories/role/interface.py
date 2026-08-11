from typing import Protocol

from app.models.role import Role


class IRoleRepository(Protocol):

    def get_by_name(self, name: str) -> Role | None: ...
