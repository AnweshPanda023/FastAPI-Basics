from app.models.user import User
from app.core.security import hash_password
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories.user.interface import IUserRepository


class AuthService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def register(self, email: str, password: str, full_name: str) -> User:

        existing_user = self.repository.get_by_email(email)

        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = hash_password(password)

        user = User(
            email=email,
            password_hash=hashed_password,
            full_name=full_name,
        )

        return self.repository.create(user)

    def login(self, email: str, password: str):

        user = self.repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }