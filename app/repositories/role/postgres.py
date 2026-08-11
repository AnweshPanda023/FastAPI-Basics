from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.role.interface import IRoleRepository


class PostgresRoleRepository(IRoleRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> Role | None:
        return self.db.query(Role).filter(Role.name == name).first()
