from app.db.unit_of_work import UnitOfWork
from app.exceptions.auth import UserNotFoundException
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user.interface import IUserRepository


class UserService:

    def __init__(
        self,
        user_repository: IUserRepository,
        unit_of_work: UnitOfWork,
    ):
        self.user_repository = user_repository
        self.unit_of_work = unit_of_work

    def update_role(self, user_id: int, role: UserRole) -> User:
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundException()
        with self.unit_of_work:
            self.user_repository.update_role(user, role)

        return user
