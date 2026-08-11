from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user.interface import IUserRepository


class PostgresUserRepository(IUserRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        return user

    def update_role(self, user: User, role: UserRole) -> User:
        user.role = role
        self.db.flush()
        return user

    def get_all(
        self,
        offset: int,
        limit: int,
        search: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> list[User]:

        query = self.db.query(User)

        if search:
            search = search.strip()

            query = query.filter(
                or_(
                    User.email.ilike(f"%{search}%"),
                    User.full_name.ilike(f"%{search}%"),
                )
            )

        if role is not None:
            query = query.filter(User.role == role)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        return query.order_by(User.id).offset(offset).limit(limit).all()

    def count_all(
        self,
        search: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> int:

        query = self.db.query(User)

        if search:
            search = search.strip()

            query = query.filter(
                or_(
                    User.email.ilike(f"%{search}%"),
                    User.full_name.ilike(f"%{search}%"),
                )
            )

        if role is not None:
            query = query.filter(User.role == role)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        return query.count()
