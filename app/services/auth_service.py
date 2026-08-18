from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import IntegrityError
from app.db.unit_of_work import UnitOfWork
from app.exceptions.auth import (
    InvalidCredentialsException,
    RoleNotFoundException,
    UserNotFoundException,
    InvalidRefreshTokenException,
    RefreshTokenExpiredException,
    EmailAlreadyExistsException,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.core.security import generate_refresh_token, hash_password, hash_refresh_token
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories.refresh_token.interface import IRefreshTokenRepository
from app.repositories.role.interface import IRoleRepository
from app.repositories.user.interface import IUserRepository
from app.core.config import settings


class AuthService:

    def __init__(
        self,
        user_repository: IUserRepository,
        role_repository: IRoleRepository,
        refresh_token_repository: IRefreshTokenRepository,
        unit_of_work: UnitOfWork,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.refresh_token_repository = refresh_token_repository
        self.unit_of_work = unit_of_work

    # register a new user
    def register(
        self,
        email: str,
        password: str,
        full_name: str,
    ) -> User:

        email = email.strip().lower()

        existing_user = self.user_repository.get_by_email(email)

        if existing_user:
            raise EmailAlreadyExistsException()

        default_role = self.role_repository.get_by_name("user")

        if default_role is None:
            raise RoleNotFoundException("Default user role is not configured")

        hashed_password = hash_password(password)

        user = User(
            email=email,
            password_hash=hashed_password,
            full_name=full_name.strip(),
            role=default_role,
        )

        try:
            with self.unit_of_work:
                self.user_repository.create(user)

        except IntegrityError:
            raise EmailAlreadyExistsException()

        self.unit_of_work.refresh(user)

        return user

    def login(
        self,
        email: str,
        password: str,
    ):

        email = email.strip().lower()

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise InvalidCredentialsException()

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsException()
        access_token = create_access_token({"sub": str(user.id)})

        refresh_token = generate_refresh_token()
        refresh_token_hash = hash_refresh_token(refresh_token)

        refresh_token_entity = RefreshToken(
            user_id=user.id,
            token_hash=refresh_token_hash,
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.refresh_token_expire_days),
        )

        with self.unit_of_work:
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
            raise InvalidRefreshTokenException()

        if token.expires_at < datetime.now(timezone.utc):
            raise RefreshTokenExpiredException()

        user = self.user_repository.get_by_id(token.user_id)

        if user is None:
            raise UserNotFoundException()

        access_token = create_access_token({"sub": str(user.id)})

        new_refresh_token = generate_refresh_token()

        new_hash = hash_refresh_token(new_refresh_token)

        new_entity = RefreshToken(
            user_id=user.id,
            token_hash=new_hash,
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.refresh_token_expire_days),
        )

        with self.unit_of_work:
            self.refresh_token_repository.revoke(token)
            self.refresh_token_repository.create(new_entity)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
