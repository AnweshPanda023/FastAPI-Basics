from datetime import datetime, timedelta, timezone

from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.core.security import generate_refresh_token, hash_password, hash_refresh_token
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories.refresh_token.interface import IRefreshTokenRepository
from app.repositories.user.interface import IUserRepository
from app.core.config import settings


class AuthService:
    def __init__(
        self,
        user_repository: IUserRepository,
        refresh_token_repository: IRefreshTokenRepository,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

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

        return self.user_repository.create(user)

    def login(
        self,
        email: str,
        password: str,
    ):

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password")

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )

        refresh_token = generate_refresh_token()

        refresh_token_hash = hash_refresh_token(refresh_token)

        refresh_token_entity = RefreshToken(
            user_id=user.id,
            token_hash=refresh_token_hash,
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.refresh_token_expire_days),
        )

        self.refresh_token_repository.create(refresh_token_entity)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh(
        self,
        refresh_token: str,
    ):

        token_hash = hash_refresh_token(refresh_token)

        token = self.refresh_token_repository.get_by_hash(token_hash)

        if token is None:
            raise ValueError("Invalid refresh token")

        if token.expires_at < datetime.now(timezone.utc):
            raise ValueError("Refresh token expired")

        self.refresh_token_repository.revoke(token)

        new_refresh_token = generate_refresh_token()

        new_hash = hash_refresh_token(new_refresh_token)

        new_refresh_token_entity = RefreshToken(
            user_id=token.user_id,
            token_hash=new_hash,
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.refresh_token_expire_days),
        )

        self.refresh_token_repository.create(new_refresh_token_entity)

        user = self.user_repository.get_by_id(token.user_id)

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
