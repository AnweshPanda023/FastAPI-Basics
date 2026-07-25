from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, oauth2_scheme
from app.db.database import get_db
from app.models.user import User
from app.repositories.refresh_token.postgres import PostgresRefreshTokenRepository
from app.repositories.user.interface import IUserRepository
from app.repositories.user.postgres import PostgresUserRepository
from app.services.auth_service import AuthService
from app.repositories.refresh_token.interface import IRefreshTokenRepository


def get_user_repository(
    db: Session = Depends(get_db),
) -> IUserRepository:
    return PostgresUserRepository(db)


def get_refresh_token_repository(
    db: Session = Depends(get_db),
) -> IRefreshTokenRepository:

    return PostgresRefreshTokenRepository(db)


def get_auth_service(
    user_repository: IUserRepository = Depends(get_user_repository),
    refresh_token_repository: IRefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
) -> AuthService:

    return AuthService(
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: IUserRepository = Depends(get_user_repository),
) -> User:

    payload = decode_access_token(token)

    user_id = int(payload["sub"])

    user = repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user